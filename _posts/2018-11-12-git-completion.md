---
layout: post
title: "Mac 环境下 git 如何自动补全"
description: "本来不想写这个，但是发现Google搜出来的都不太对，还是简单记录下吧。"
figure: "https://res.cloudinary.com/cyeam/image/upload/v1540351553/cyeam/git.png"
category: "Tool"
tags: ["git"]
---

* 目录
{:toc}
---

### 安装 bash-completion

```
brew install bash-completion
```

将下面代码添加到~/.bash_profile（如果没有该文件，新建一个）。

```
# git auto completition
if [ -f ~/.git-completion.bash ]; then
  . ~/.git-completion.bash
fi
```

### 安装 git-completion.bash

这个文件不能随便安装，网上的教程都是用git参数的master分支，这是不对的，这个版本需要和当前系统安装的git版本对应。

```
git version
```

看看自己的版本是什么，我的是`2.17.1`，就需要用这个[版本的脚本](https://raw.githubusercontent.com/git/git/v2.17.1/contrib/completion/git-completion.bash)。将脚本报存到`~/.git-completion.bash`里面，然后执行：

```
source ~/.git-completion.bash
source ~/.bash_profile
```

这样就可以咯，按下Tab键就可以提示啦。

```
$ git che
checkout      cherry        cherry-pick
```

---


{% include JB/setup %}
