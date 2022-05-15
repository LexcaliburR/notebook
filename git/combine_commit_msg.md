<!--
 * @Author: Lexcaliburr lishiqi0111@gmail.com
 * @Date: 2022-05-15 16:38:31
 * @LastEditors: Lexcaliburr lishiqi0111@gmail.com
 * @LastEditTime: 2022-05-15 17:04:43
 * @FilePath: /notebook/git/combine_commit_msg.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
# 将多个commit的信息进行combine
### 1.git rebase
```sh
git rebase -i HEAD~{3} # 括号中的数字为需要合并的commit,3为从当前head开始的最近3次提交

```

### 2.设置combine方式
2.1 输入上面的命令后,ubuntu下默认进入nano文本编辑器
```sh
pick 1baa61b test 1
pick 689ed66 add test file 2
pick d0ef07b commit 3

# Rebase 8c7ebb1..d0ef07b onto 8c7ebb1 (3 commands)
#
# Commands:
# p, pick = use commit   # 保留当前commit,包括信息
# r, reword = use commit, but edit the commit message # 保留当前commit文件变更,但是修改提交的commit的信息
# e, edit = use commit, but stop for amending 
# s, squash = use commit, but meld into previous commit # 保留当前commit的文件变更,删除commit信息以及commit记录
# f, fixup = like "squash", but discard this commit's log message
# x, exec = run command (the rest of the line) using shell
# d, drop = remove commit
#
# These lines can be re-ordered; they are executed from top to bottom.
#
# If you remove a line here THAT COMMIT WILL BE LOST.
#
# However, if you remove everything, the rebase will be aborted.
#
# Note that empty commits are commented out

```
2.2 将上述文件进行如下修改可以实现commit的合并
```sh
drop 1baa61b test 1   # 删除这次commit,因为该次commit只是提交了一个测试文件
drop 689ed66 add test file 2 # 删除这次commit,因为这次commit只是提交了一个测试文件
pick d0ef07b add how combine commit # 压缩这3次commit记录,

```
2.3如果有其他提交记录的压缩方式
```sh
drop 1baa61b test 1   # 删除这次commit,因为该次commit只是提交了一个测试文件
drop 689ed66 add test file 2 # 删除这次commit,因为这次commit只是提交了一个测试文件
pick sadfasf add test file 2 # 有效变更,需要被压缩
squash dhjdgfg add test file 2 # 有效变更,需要被压缩 需要保留的第一个改为pick,需要被压缩的改为squash
squash d0ef07b add how combine commit # 压缩这3次commit记录,

```
### 3.保存
在nano 编辑器下  
ctrl+X 进入Exit  
Y 保存选项  
ctrl+T 选择保存的文件  
git rebase --continue 编辑新的msg信息
