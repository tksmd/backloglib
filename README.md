# What's backloglib

(英語の下に日本文が記載されています)

backloglib is a simple [Backlog](http://backlogtool.com) API wrapper for python. backloglib offers simple types for each API call (like Issue or Project). backloglib helps you to use Backlog API in that

* it enables method completion by IDE like Pydev or PyCharm
* it secures your code with type validation before calling API

## Update

* 2014/03/05 0.2.3 released ( moved from https://code.google.com/p/backloglib/ )
* 2010/11/06 0.2.1 released

For more details, refer to [Release Notes](https://github.com/tksmd/backloglib/wiki/ReleaseNotes).

## Install

```
$ pip install backloglib
```

## How to use

Basically you should follow the steps below

1. Initialize Backlog object with your space, username and password
2. call API method with the Backlog object

Information about API method is provided [here](http://www.backlog.jp/api). Here's an example how to call Backlog API with backloglib. Method names in Backlog API are converted from camel case to snake case in backloglib.

```python
import backloglib

# ----- 1. initialize backlog object -----

backlog = backloglib.Backlog("spacename","username","password")

# ----- 2. API call -----

# get projects
projects = backlog.get_projects()
project = backlog.get_project("YOUR_PROJECT")
project = backlog.get_project(1) # YOUR_PROJECT's ID

# get categories
components = backlog.get_components(project.id)

# get versions (milestones)
versions = backlog.get_versions(project.id)

# get users
users = backlog.get_users(project.id)

# get issue types
issue_types = backlog.get_issue_types(project.id)

# get issues
issue = backlog.get_issue("ISSUE_NAME")
issue = backlog.get_issue(1) # ISSUE_NAME's ID

# get comments
comments = backlog.get_comments(issue.id)

# get number of issues that matche given condition
count = backlog.count_issue({
                            "projectId":project.id
                            })

# find issues that matche given condition
issues = backlog.find_issue({
                            "projectId":project.id
                            })

# create an issue
issue = backlog.create_issue({
                             "projectId":project.id,
                             "summary":u"Issue summary"
                             })

# update an issue
updated = backlog.update_issue({
                               "key":issue.key,
                               "summary":u"Update issue summary"
                               })

# update issue status
updated = backlog.switch_status({
                               "key":issue.key,
                               "statusId":backloglib.Status.COMPLETED
                               })
```

To use administrator's API, you have to initialize a BacklogAdmin object instead Backlog object.

```python
import backloglib

# ----- 1. initialize backlog object -----

backlog = backloglib.BacklogAdmin("spacename","username","password")

# ----- 2. API call -----

# get users which belongs to projects
project_users = backlog.get_project_users()
```

# For Developers

## Test

To run test class
```
$ PYTHONPATH=src:test python -m unittest -v backloglibtest.test_Backlog
```

To run single method
```
$ PYTHONPATH=src:test python -m unittest -v backloglibtest.test_Backlog.BacklogTest.test_get_projects1
```

# backloglib とは

backloglib は [Backlog](http://www.backlog.jp) の API にアクセスするための python のクライアントライブラリです。

## 更新情報

* 2014/03/05 0.2.3 をリリースしました ( https://code.google.com/p/backloglib/ から移転しました )
* 2010/11/06 0.2.1 をリリースしました

リリースの詳細については [リリースノート](https://github.com/tksmd/backloglib/wiki/ReleaseNotes) を参照ください。

## 利点

ライブラリを使うメリットとしては、

 * Pydev などの IDE を使うと、メソッドの補完をしてくれる事
 * 実際の API コールの前に、引数の名前チェックをする事 (= 引数に不足あればエラーが出ます)

といった辺りです。非常にシンプルなラッパーという位置づけです。

## インストール

### 前提条件

0.2.1 より python 2.5 以上でのご利用を前提としています。2.5 と 2.6 にて動作を確認しています。標準で提供されている xmlrpclib 以外に依存しているライブラリはありません。

### pip を利用する場合

```
$ pip install backloglib
```

### setup.py を利用する場合

```
# ダウンロードしたアーカイブを展開
$ tar zxvf backloglib-<ver>.tar.gz
# setup.py を実行
$ cd backloglib-<ver>
$ python setup.py install
```

### easy_install を利用する場合

[easy_install](http://peak.telecommunity.com/DevCenter/EasyInstall) を利用する場合は、まずお手元の環境に [setuptools](http://pypi.python.org/pypi/setuptools) をインストールした後に以下を実行してください。

```
# easy_install を実行
$ easy_install backloglib
```

## 使い方

基本的な使い方は以下の 2 ステップとなります。

* backlog オブジェクトを生成
* [API](http://www.backlog.jp/api/) に従ったメソッド呼び出し

例としては以下のようになります。各メソッドの詳細については上記の API のページの詳細をご覧ください。backloglib で呼び出すメソッド名は、基本的に Backlog API のキャメル記法をアンダースコアに、大文字を全て小文字に置き換えたものになっています。

```python
import backloglib

# ----- 1. backlog オブジェクトを生成 -----

backlog = backloglib.Backlog("spacename","username","password")

# ----- 2. API に従ったメソッド呼び出し -----

# プロジェクトの取得
projects = backlog.get_projects()
project = backlog.get_project("YOUR_PROJECT")
project = backlog.get_project(1) # YOUR_PROJECT's ID

# コンポーネントの取得
components = backlog.get_components(project.id)

# バージョンの取得
versions = backlog.get_versions(project.id)

# ユーザの取得
users = backlog.get_users(project.id)

# 課題タイプの取得
issue_types = backlog.get_issue_types(project.id)

# 課題の取得
issue = backlog.get_issue("ISSUE_NAME")
issue = backlog.get_issue(1) # ISSUE_NAME's ID

# コメントの取得
comments = backlog.get_comments(issue.id)

# 課題数の取得
count = backlog.count_issue({
                            "projectId":project.id
                            })

# 課題の検索
issues = backlog.find_issue({
                            "projectId":project.id
                            })

# 課題の作成
issue = backlog.create_issue({
                             "projectId":project.id,
                             "summary":u"課題のサマリ"
                             })

# 課題の更新
updated = backlog.update_issue({
                               "key":issue.key,
                               "summary":u"サマリの更新"
                               })

# ステータスの更新
updated = backlog.switch_status({
                               "key":issue.key,
                               "statusId":backloglib.Status.COMPLETED
                               })
```

管理者用 API (backlog.admin ではじまるもの) は以下のように !BacklogAdmin オブジェクトを利用します。利用方法は上記と変わりません。

```
import backloglib

# ----- 1. backlog オブジェクトを生成 -----

backlog = backloglib.BacklogAdmin("spacename","username","password")

# ----- 2. API に従ったメソッド呼び出し -----

# プロジェクトユーザの取得
project_users = backlog.get_project_users()
```

## 参考

0.2.2 以前の情報については [http://code.google.com/p/backloglib/](http://code.google.com/p/backloglib/) をご覧ください
