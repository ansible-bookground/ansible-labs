# 4.2 ネットワークの自動化 補足情報

## 「4.2.4 ハンズオン環境の準備」

### マネージドノードの再構築手順

マネージドノードをクリーンな状態に戻すために、再度プロビジョニングする場合は以下の手順を実行してください。

マネージドノードの仮想マシンを削除する:

```shell
$ cd <project root>/chapter4/network/vagrant
$ vagrant destroy
```

マネージドノードの仮想マシンをプロビジョニングする:

```shell
$ vagrant up
```

コントロールノードにログインする:

```shell
$ cd <project root>/chapter2/vagrant
$ vagrant ssh
```

コントロールノードからマネージドノードに対してSSH公開鍵を登録する:

```shell
$ cd ~/ansible-labs/chapter4/network/playbooks
$ ansible-playbook -i inventory.yml init.yml
```
