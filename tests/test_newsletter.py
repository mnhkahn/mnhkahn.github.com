import copy
import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('newsletter', Path(__file__).parents[1] / 'scripts/send_newsletter.py')
n = importlib.util.module_from_spec(spec)
spec.loader.exec_module(n)

POST = {'id': '/new', 'title': 'Go <AI>', 'description': 'A & B', 'url': 'https://blog.cyeam.com/new', 'newsletter': True}


class Store:
    def __init__(self):
        self.value = {'known_ids': ['/old'], 'pending': None}

    def save(self, value):
        self.value = copy.deepcopy(value)


class Mailchimp:
    def __init__(self, status='save', ready=True, fail_send=False):
        self.campaign = {'id': 'c1', 'status': status}
        self.calls = []
        self.ready = ready
        self.fail_send = fail_send

    def find_campaign(self, *args):
        return self.campaign

    def call(self, path, method='GET', data=None):
        self.calls.append((method, path, data))
        if path.endswith('/send-checklist'):
            return {'is_ready': self.ready}
        if path.endswith('/actions/send'):
            self.campaign['status'] = 'sent'
            if self.fail_send:
                raise RuntimeError('Response lost after server accepted send')
        return self.campaign


class NewsletterTests(unittest.TestCase):
    def setUp(self):
        self.manifest = {'audience_id': '6ef0d9748c', 'posts': [POST]}

    def test_edits_and_opt_out_are_not_new_posts(self):
        state = {'known_ids': ['/new']}
        self.assertEqual(n.select_posts(state, [POST]), [])
        self.assertEqual(n.select_posts({'known_ids': []}, [{**POST, 'newsletter': False}]), [])

    def test_batch_identity_does_not_depend_on_order_or_edits(self):
        other = {**POST, 'id': '/other'}
        self.assertEqual(n.campaign_title([POST, other]), n.campaign_title([other, {**POST, 'title': 'edited'}]))

    def test_template_escapes_content_and_has_unsubscribe(self):
        rendered = n.render_email([POST])
        self.assertIn('Go &lt;AI&gt;', rendered)
        self.assertIn('A &amp; B', rendered)
        self.assertIn('*|UNSUB|*', rendered)
        with self.assertRaises(ValueError):
            n.render_email([{**POST, 'url': 'javascript:alert(1)'}])

    def test_new_post_sends_once(self):
        store, mc = Store(), Mailchimp()
        n.deliver(store, copy.deepcopy(store.value), self.manifest, mc)
        n.deliver(store, copy.deepcopy(store.value), self.manifest, mc)
        self.assertEqual(sum(path.endswith('/actions/send') for _, path, _ in mc.calls), 1)
        self.assertIn('/new', store.value['known_ids'])

    def test_retry_after_ambiguous_send_uses_same_campaign(self):
        store, mc = Store(), Mailchimp(fail_send=True)
        with self.assertRaises(RuntimeError):
            n.deliver(store, copy.deepcopy(store.value), self.manifest, mc)
        self.assertEqual(store.value['pending']['campaign_id'], 'c1')
        n.deliver(store, copy.deepcopy(store.value), self.manifest, mc)
        self.assertEqual(sum(path.endswith('/actions/send') for _, path, _ in mc.calls), 1)
        self.assertIsNone(store.value['pending'])

    def test_failed_checklist_keeps_pending_without_sending(self):
        store, mc = Store(), Mailchimp(ready=False)
        with self.assertRaises(RuntimeError):
            n.deliver(store, copy.deepcopy(store.value), self.manifest, mc)
        self.assertIsNotNone(store.value['pending'])
        self.assertFalse(any(path.endswith('/actions/send') for _, path, _ in mc.calls))

    def test_already_sending_is_not_sent_again(self):
        store, mc = Store(), Mailchimp(status='sending')
        n.deliver(store, copy.deepcopy(store.value), self.manifest, mc)
        self.assertFalse(any(path.endswith('/actions/send') for _, path, _ in mc.calls))


if __name__ == '__main__':
    unittest.main()
