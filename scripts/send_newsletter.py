"""Send newly deployed posts. State lives on the dedicated newsletter-state branch."""
import base64
import hashlib
import html
import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen

STATE_BRANCH = "newsletter-state"
MANIFEST_URL = "https://blog.cyeam.com/newsletter.json"


def request_json(url, token=None, method="GET", data=None):
    headers = {"Accept": "application/json", "User-Agent": "Cyeam-Newsletter"}
    if token:
        headers["Authorization"] = "Bearer " + token
    body = None
    if data is not None:
        headers["Content-Type"] = "application/json"
        body = json.dumps(data).encode()
    try:
        with urlopen(Request(url, data=body, headers=headers, method=method), timeout=45) as response:
            content = response.read()
            return json.loads(content) if content else None
    except HTTPError as error:
        # Keep credentials, subscriber data and response bodies out of Actions logs.
        raise RuntimeError(f"{method} {urlsplit(url).path}: HTTP {error.code}") from error


class StateStore:
    def __init__(self):
        self.base = "https://api.github.com/repos/" + os.environ["GITHUB_REPOSITORY"]
        self.token = os.environ["GH_TOKEN"]
        self.sha = None

    def load(self):
        try:
            result = request_json(self.base + "/contents/state.json?ref=" + STATE_BRANCH, self.token)
        except RuntimeError as error:
            if isinstance(error.__cause__, HTTPError) and error.__cause__.code == 404:
                return None
            raise
        self.sha = result["sha"]
        return json.loads(base64.b64decode(result["content"]))

    def save(self, state):
        if self.sha is None:
            try:
                request_json(self.base + "/git/ref/heads/" + STATE_BRANCH, self.token)
            except RuntimeError as error:
                if not isinstance(error.__cause__, HTTPError) or error.__cause__.code != 404:
                    raise
                repo = request_json(self.base, self.token)
                ref = request_json(self.base + "/git/ref/heads/" + repo["default_branch"], self.token)
                # This branch is deliberately separate from the Pages source branch.
                request_json(self.base + "/git/refs", self.token, "POST", {
                    "ref": "refs/heads/" + STATE_BRANCH, "sha": ref["object"]["sha"],
                })
        data = {
            "message": "Update blog newsletter delivery state",
            "branch": STATE_BRANCH,
            "content": base64.b64encode(json.dumps(state, ensure_ascii=False, indent=2).encode()).decode(),
        }
        if self.sha:
            data["sha"] = self.sha
        result = request_json(self.base + "/contents/state.json", self.token, "PUT", data)
        self.sha = result["content"]["sha"]


class Mailchimp:
    def __init__(self, key):
        server = key.rsplit("-", 1)[-1]
        if not server.startswith("us") or not server[2:].isdigit():
            raise ValueError("Invalid Mailchimp data center suffix")
        self.base = f"https://{server}.api.mailchimp.com/3.0/"
        self.key = key

    def call(self, path, method="GET", data=None):
        return request_json(self.base + path, self.key, method, data)

    def find_campaign(self, audience, title):
        offset = 0
        while True:
            result = self.call("campaigns?" + urlencode({
                "list_id": audience, "count": 100, "offset": offset,
                "fields": "campaigns.id,campaigns.status,campaigns.settings.title,total_items",
            }))
            matches = [c for c in result["campaigns"] if c["settings"]["title"] == title]
            if len(matches) > 1:
                raise RuntimeError("Multiple matching campaigns; resolve in Mailchimp before retrying")
            if matches:
                return matches[0]
            offset += len(result["campaigns"])
            if offset >= result["total_items"] or not result["campaigns"]:
                return None


def campaign_title(posts):
    identity = json.dumps(sorted(p["id"] for p in posts), ensure_ascii=False)
    return "cyeam-blog-" + hashlib.sha256(identity.encode()).hexdigest()[:24]


def render_email(posts):
    cards = []
    for post in posts:
        url = post["url"]
        if not url.startswith("https://blog.cyeam.com/"):
            raise ValueError("Post URL must belong to the blog")
        cards.append(
            '<article style="margin:28px 0">'
            f'<h2 style="font-size:22px"><a href="{html.escape(url, quote=True)}">{html.escape(post["title"])}</a></h2>'
            f'<p style="color:#555">{html.escape(post["description"])}</p>'
            f'<p><a href="{html.escape(url, quote=True)}">阅读全文 →</a></p></article>'
        )
    return (
        '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1"></head>'
        '<body style="margin:0;background:#f5f6f8;font-family:Arial,sans-serif;line-height:1.7">'
        '<div style="max-width:600px;margin:24px auto;padding:28px;background:#fff">'
        '<p style="color:#666">CYEAM · 博客更新</p><h1 style="font-size:26px">新文章，与你分享。</h1>'
        + "".join(cards)
        + '<hr><p style="font-size:12px;color:#777">你收到此邮件，是因为订阅了 Cyeam 博客更新。<br>'
        '<a href="*|UNSUB|*">退订</a> · <a href="*|UPDATE_PROFILE|*">更新订阅偏好</a><br>'
        '*|LIST:ADDRESS|*</p></div></body></html>'
    )


def select_posts(state, posts):
    known = set(state["known_ids"])
    return [p for p in posts if p["id"] not in known and p.get("newsletter", True)]


def deliver(store, state, manifest, mailchimp):
    audience_id = manifest["audience_id"]
    pending = state.get("pending")
    if not pending:
        posts = select_posts(state, manifest["posts"])
        if not posts:
            state["known_ids"] = sorted(set(state["known_ids"]) | {p["id"] for p in manifest["posts"]})
            store.save(state)
            print("No new posts to send")
            return
        pending = {"posts": posts, "title": campaign_title(posts), "campaign_id": None}
        state["pending"] = pending
        store.save(state)

    campaign = (mailchimp.call("campaigns/" + pending["campaign_id"]) if pending["campaign_id"]
                else mailchimp.find_campaign(audience_id, pending["title"]))
    if campaign is None:
        defaults = mailchimp.call("lists/" + audience_id)["campaign_defaults"]
        posts = pending["posts"]
        subject = ("Cyeam 新文章：" + posts[0]["title"] if len(posts) == 1
                   else f"Cyeam 博客更新：{len(posts)} 篇新文章")
        campaign = mailchimp.call("campaigns", "POST", {
            "type": "regular", "recipients": {"list_id": audience_id},
            "settings": {"title": pending["title"], "subject_line": subject[:150],
                         "from_name": defaults["from_name"], "reply_to": defaults["from_email"],
                         "preview_text": posts[0]["description"][:150]},
        })
    pending["campaign_id"] = campaign["id"]
    store.save(state)
    status = campaign["status"]
    if status == "save":
        mailchimp.call("campaigns/" + campaign["id"] + "/content", "PUT", {
            "html": render_email(pending["posts"]),
        })
        checklist = mailchimp.call("campaigns/" + campaign["id"] + "/send-checklist")
        if not checklist["is_ready"]:
            print("Mailchimp campaign is not ready. Check its delivery checklist in the dashboard.")
            raise RuntimeError("Mailchimp send checklist failed; draft retained for retry")
        # Never blindly retry this POST: on an ambiguous network failure, the next run
        # retrieves this SAME campaign and checks status before deciding what to do.
        mailchimp.call("campaigns/" + campaign["id"] + "/actions/send", "POST")
    elif status not in ("sent", "sending"):
        raise RuntimeError(f"Campaign status {status!r} requires inspection in Mailchimp")

    state["known_ids"] = sorted(set(state["known_ids"]) | {p["id"] for p in pending["posts"]})
    state["last_campaign_id"] = campaign["id"]
    state["pending"] = None
    store.save(state)
    print(f"Campaign {campaign['id']} submitted/already sent: {len(pending['posts'])} post(s)")


def main():
    # A local manifest can be used for preview without any Mailchimp credentials.
    preview_path = os.environ.get("NEWSLETTER_MANIFEST")
    manifest = (json.loads(Path(preview_path).read_text()) if preview_path
                else request_json(MANIFEST_URL + "?run=" + os.environ.get("GITHUB_RUN_ID", "preview")))
    expected = os.environ.get("EXPECTED_REVISION")
    if expected and manifest.get("revision") != expected:
        raise RuntimeError("Live manifest does not match this deployment; no mail sent")
    if manifest.get("audience_id") != "6ef0d9748c":
        raise RuntimeError("Unexpected newsletter audience")
    dry_run = os.environ.get("DRY_RUN", "true").lower() != "false"
    if dry_run and preview_path:
        print(render_email(manifest["posts"][:3]))
        return
    store = StateStore()
    state = store.load()
    if state is None:
        if not dry_run:
            store.save({"known_ids": sorted(p["id"] for p in manifest["posts"]), "pending": None})
        print(f"{'Would initialize' if dry_run else 'Initialized'} baseline: {len(manifest['posts'])} existing posts; no mail sent")
        return
    if dry_run:
        posts = (state.get("pending") or {}).get("posts", select_posts(state, manifest["posts"]))
        print(f"Preview: {len(posts)} new post(s); no API writes or sends")
        for post in posts:
            print(post["title"], post["url"])
        return
    mailchimp = Mailchimp(os.environ["MAILCHIMP_API_KEY"])
    # Finish a retained batch first, then handle any newer posts from this deployment.
    deliver(store, state, manifest, mailchimp)
    if select_posts(state, manifest["posts"]):
        deliver(store, state, manifest, mailchimp)


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, ValueError, KeyError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
