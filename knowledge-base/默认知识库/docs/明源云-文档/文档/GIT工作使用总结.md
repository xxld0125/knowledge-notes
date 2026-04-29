#### 目录
+ 简介
+ 常用操作命令
+ 常见问题
+ 图形化操作
+ .gitignore文件
+ 参考文档

---





#### 一、简介
Git 是一种分布式版本控制系统，它可以不受网络连接的限制，加上其它众多优点，目前已经成为程序开发人员做项目版本管理时的首选，非开发人员也可以用 Git 来做自己的文档版本管理工具。

![](https://cdn.nlark.com/yuque/0/2022/webp/25743026/1649485444930-9ee97e91-82a4-455a-bda0-2756e8415794.webp)

+ **Workspace**:工作区，平时进行开发改动的地方，是当前看到的最新内容，在开发的过程也就是对工作区的操作。
+ **Index**:暂存区，当执行git add的命后，工作区的文件就会移到暂存区，暂存区标记了当前工作区中那些内容是被Git管理的，当完成某个需求或功能后需要提交代码，第一步就是通过git add先提交到暂存区。
+ **Repository**:本地仓库，位于自己的电脑上，通过**git commit**提交暂存区的内容，会进入本地仓库中。
+ **Remote**:远程仓库，用来托管代码的服务器，远程仓库的内容能够被分布在多个地点的处于协作关系的本地仓库修改，本地仓库修改完代码后通过git push命令同步代码到远程仓库。
+ **.git**：版本库，在git init时创建，创建时会自动创建master分支，并且将指针指向master分支 

---

#### 二、常用操作命令
##### 1、日常开发常用命令
+ git add

```git
# 添加某个文件到暂存区，后面可以跟多个文件，以空格区分
git add xxx
# 添加当前更改的所有文件到暂存区。
git add .
# 进入交互模式
git add -p
```

+ git commit

```bash
# 提交暂存的更改，会新开编辑器进行编辑
git commit 
# 提交暂存的更改，并记录下备注
git commit -m "you message"
# 等同于 git add . && git commit -m
git commit -am
# 对最近一次的提交的信息进行修改,此操作会修改commit的hash值
git commit --amend
```

+ git push

```git
# 将本地分支推送到远程仓库
git push [remote-name] [branch-name]
# 将本地分支推送到远程仓库的不同分支名
git push <remote-name> <local-branch>:<remote-branch>
# 删除远程分支
git push [remote-name] :<remote-branch>(省略了本地分支，相当于将空白内容推送给远程分支，等用于删掉了远程分支)
```

+ git pull

```git
# 从远程仓库拉取代码并合并到本地，可简写为 git pull 等同于 git fetch && git merge 
git pull <远程主机名> <远程分支名>:<本地分支名>
# 使用rebase的模式进行合并，等用于 git fetch && git rebase
git pull --rebase <远程主机名> <远程分支名>:<本地分支名>
```

+ git fetch

与 git pull 不同的是 git fetch 操作仅仅只会拉取远程的更改，不会自动进行 merge 操作。对你当前的代码没有影响

```git
# 获取远程仓库特定分支的更新
git fetch <远程主机名> <分支名>
# 获取远程仓库所有分支的更新
git fetch --all
```

+ git branch

```git
# 新建本地分支，但不切换
git branch <branch-name> 
# 将新建分支，发布到远程
git push --set-upstream origin <branch-name>

# 将本地分支推送到远程
git push origin <branch-name>
# 查看本地分支
git branch
# 查看远程分支
git branch -r
# 查看本地和远程分支
git branch -a
# 删除本地分支
git branch -D <branch-name>
# 删除远程分支
git push origin --delete <branch-name>
# 重新命名分支
git branch -m <old-branch-name> <new-branch-name>
# 查询各分支最后一个提交对象的信息
git branch -v
# 查询那些分支已经(/还没)合并到当前分支
git branch --merged
git branch --no-merged
```

+ git checkout

checktout命令用于从本地仓库（或者暂存区） 中拷贝文件到工作区，也可用于切换分支；

```git
# 将当前提交节点的父节点中的files复制到工作目录并加到暂存区；
git checktout HEAD files
# 切换本地分支
git checktout branch
# 新建并切换到新建分支上
git checkout -b branch
# 在远程分支的基础上创建新的本地分支
git checkout -b <branch-name> <remore-name>/<branch-name>
# 撤销工作区的文件
git checkout -- [file-name];
```

+ git reset

reset命令会把当前分支指向另一个位置，并且有选择的变动工作目录和索引。也用来在从本地仓库复制文件索引，而不动工作目录。

```git
# 没有给出提交点的版本号，默认用HEAD,会回滚最后一次提交
git reset
# 指定版本的索引 
git reset HEAD~3
# 回滚的文件复制到工作区
git reset HEAD --mixed
# 回滚的文件复制到暂存区
git reset HEAD --soft
# 不保存回滚的文件
git reset HEAD --hard
# 工作效果和带文件名的checkout类似，除了索引被更新
git reset --files
```

+ git merge

merge命令把不同分支合并起来，合并前索引必须和当前提交相同。如果另一个分支是当前提交的祖父节点，那么合并命令将什么也不做。另一种情况是如果当前提交时另一个分支的祖父节点，就导致fast-forward合并。指向只是简单的移动，并生成一个新的提交。

```git
# 合并其他分支
git merge branch
# 合并远程分支到当前分支
git merge <remote-name>/<branch-name> 如：git merge origin/master
```

+ git rm

```git
# 删除工作区文件，并且也从暂存区删除对应的文件记录；
git rm xxx(多个文件用空格区分)
# 从暂存区删除文件，但是工作区依然还有改文件
git rm --cached xxx
```



##### 2、首次搭建环境命令
+ git init 创建一个新的本地仓库

```git
# 在当前目录新建一个Git代码库
git init

# 新建一个目录，将其初始化为Git代码库
git init [project-name]
```

+ git clone 从远程git仓库复制项目

```git
#从远程仓库复制项目
git clone [仓库地址]

# 从远程仓库复制项目重命名
git clone [仓库地址] newName

# 从远程仓库指定分支复制项目
git clone -b [branch-name] [仓库地址]
```

+ git config 查询配置信息

```git
# 列出当前配置
git config --list
# 列出repository配置
git config --local --list
# 列出全局配置
git config --global --list
# 列出系统配置
git config --system --list

# 配置用户信息
# 配置用户名
git config --global user.name "name"
# 配置用户邮箱
git config --global user.email "email"

# 其他配置
# 配置解决冲突时使用哪种差异分析工具，比如要使用vimdiff
git config --global merge.tool vimdiff
# 配置git 命令输入为彩色时
git config --global color.ui auto
# 配置git使用的文本编辑器
git config --global core.editor vi
```



##### 3、其他命令
+ git mv

```git
# 重命名文件，并将已改名文件提交到暂存区
git mv oldname newname
```

+ git status

```git
# 查询当前工作区所有文件的状态
git status
```

+ git diff

```git
# 指定文件在工作区和暂存区之间差异比较
git diff xxx
# 比较暂存区与上一版本的差异
git diff --cached
# 指定文件在暂存区和本地仓库的不同
git diff xxx --cached
```

+ git tag

Git 使用的标签有两种类型：**轻量级的（lightweight）和含附注的（annotated）**。轻量级标签就像是个不会变化的分支，实际上它就是个指向特定提交对象的引用。而含附注标签，实际上是存储在仓库中的一个独立对象，它有自身的校验和信息，包含着标签的名字，电子邮件地址和日期，以及标签说明，标签本身也允许使用 GNU Privacy Guard (GPG) 来签署或验证。一般我们都建议使用含附注型的标签，以便保留相关信息；当然，如果只是临时性加注标签，或者不需要旁注额外信息，用轻量级标签也没问题。

```git
# 列出现在所有的标签
git tag
# 使用指定的搜索模式列出所有符合条件的标签
git tag -l "v1.1.*"
# 创建一个含附注类型的标签
git tag -a "version" -m "version msg"
# 查看对应标签的版本信息，并连同显示打标签时的提交对象
git show "version"
# 将标签推送到远程仓库
git push origin "version"
# 将本地所有的标签全部推送到远程仓库中
git push origin --tags
```

+ git log 

```git
# 查看commit历史
git log
git log --summary
```

+ git remote

```git
# 查看远程仓库的url
git remote -v
# 添加远程仓库
git remote add [remote-name] [url]
# 查看远程仓库的详细信息
git remote show origin
# 修改远程仓库在本地的简称
git remote rename [old-name] [new-name]
# 移除远程仓库
git remote rm [remote-name]
```

+ git help

```git
#展示git命令大纲
git help
#展示git命令大纲全部列表
git help -a
```

---

#### 三、常见问题
##### 1、合并代码
+ rebase:rebase翻译为变基，作用和merge很相似，用于把一个分支的修改合并到当前分支上。下图介绍了经过 rebase 后提交历史的变化情况![](https://cdn.nlark.com/yuque/0/2022/webp/25743026/1649485444913-8de3fcd3-b5e3-4583-be02-b71f83f1d1b4.webp)  

+ merge:不同于 git rebase 的是，git merge 在不是 fast-forward（快速合并）的情况下，会产生一条额外的合并记录，类似 Merge branch 'xxx' into 'xxx' 的一条提交信息。![](https://cdn.nlark.com/yuque/0/2022/webp/25743026/1649485444929-790b86d6-84b4-4eb1-ad0b-733031bebba8.webp)另外，在解决冲突的时候，用 merge 只需要解决一次冲突即可，简单粗暴，而用 rebase 的时候 ，需要依次解决每次的冲突，才可以提交。
+ cherry-pick理解为“挑拣”提交，和merge合并一个分支上的所有提交有所不同，他会获得某一个分支的单笔提交，并作为一个新的提交引入到你当前的分支上。当我们需要在本地合入其他分支的提交时，如果我们不想对整个分支进行合并，而是志向将某一次合入到本地当前分支commit-hash代表某次commit的hash值。

```git
# 单个commit合入
git cherry-pick [commit-hash]

# 多个commit合入
git cherry-pick <first-commit-id>...<last-commit-id>
```

**	注：**上面写法，first-commit-id的代码不会被合并，如需合并，则使用git cherry-pick <first-commit-id>^...<last-commit-id>

总结:不建议使用rebase,产生问题是追溯困难;



##### 2、撤回提交
+ revert撤销某次操作，此操作不会修改原本的提交记录，而是会新增一条提交记录来抵消某次操作。git revert会新建一条commit信息，来撤回之前的修改。

```git
# 针对普通 commit 
git revert <commit-id>

# 针对 merge 的 commit
git revert <commit-id> -m 

# 多次回滚（前开后闭区间）
git revert [commit-id1] [commit-id2] ... 
```

+ resetgit reset会直接将提交记录退回到制定的commit上。  
总结:对于个人的 feature 分支而言，可以使用 git reset 来回退历史记录，之后使用 git push --force 进行推送到远程，但是如果是在多人协作的集成分支上，不推荐直接使用 git reset 命令，而是使用更加安全的 git revert 命令进行撤回提交。这样，提交的历史记录不会被抹去，可以安全的进行撤回。



##### 3、本地存在修改时,需要切换分支时
**git stash**

**作用：**暂存文件；

**背景**：现在你正在用你的开发 分支上开发新功能。这时，生产环境上出现了一个 bug 需要紧急修复，但是你这部分代码还没开发完，不想提交，怎么办？这个时候可以用 git stash 命令先把工作区已经修改的文件暂存起来，然后切换到修复分支上进行 bug 的修复，修复完成后，切换回 开发 分支，从堆栈中恢复刚刚保存的内容。

```git
# 把本地的改动暂存起来
git stash

# 执行存储时，添加备注，方便查找。
git stash save "message" 

# 应用最近一次暂存的修改，并删除暂存的记录
git stash pop

# 应用某个存储,但不会把存储从存储列表中删除，默认使用第一个存储,即 stash@{0}，如果要使用其他个，git stash apply stash@{$num} 。
git stash apply

# 查看 stash 有哪些存储
git stash list

# 删除所有缓存的 stash
git stash clear
```



##### 4、修改commit提交备注
```git
git commit --amend
```

---

#### 四、图形化操作
常见的有GitHub for Desktop、Source Tree、TortoiseGit等,对于使用IDE进行开发的程序员,可以直接使用IDE直接操作源代码管理系统.

前端开发可以使用vscode自带的代码及相关的插件(git graph、git-history等)

以下介绍几个比较常用操作;

1. git reset![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1649485512900-c3b887f9-eb0f-4425-b4ec-ea5a428cd668.png)
2. git stash![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1649485552787-6076015d-273b-4251-add3-700cc28a7f68.png)
3. git merge![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1649485562182-7a084dac-b4ff-4812-bb9e-6f852f27388a.png)
4. git revert![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1649485568996-af5ab179-763a-4581-8b9f-ace492a0545c.png)
5. git cherry pick![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1649485576245-222b2d6d-2774-4dc4-88a7-4917a7a04fdc.png)
6. ...

---

#### 五、忽略文件.gitignore
一般我们总会有些文件无需纳入 Git 的管理，也不希望它们总出现在未跟踪文件列表。通常都是些自动生成的文件，比如日志文件，或者编译过程中创建的临时文件等。我们可以创建一个名为 .gitignore 的文件，列出要忽略的文件模式。

```git
# 此为注释 – 将被 Git 忽略
# 忽略所有 .a 结尾的文件
*.a
# 但 lib.a 除外
!lib.a
# 仅仅忽略项目根目录下的 TODO 文件，不包括 subdir/TODO
/TODO
# 忽略 build/ 目录下的所有文件
build/
# 会忽略 doc/notes.txt 但不包括 doc/server/arch.txt
doc/*.txt
# 忽略 doc/ 目录下所有扩展名为 txt 的文件
doc/**/*.txt
```

---

#### 六、参考文档
+ [我在工作中是如何使用git的](https://juejin.cn/post/6974184935804534815)
+ [图解git](https://marklodato.github.io/visual-git-guide/index-zh-cn.html)
+ [git基本操作，一篇文章就够了！](https://juejin.cn/post/6844903598522908686)
+ [「一劳永逸」一张脑图带你掌握Git命令](https://juejin.cn/post/6869519303864123399)

