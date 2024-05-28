# linux_std_setting ロール

## 機能

Linux に対して組織のOS標準設定を適用する機能を提供。 サポート対象の Linux Distribution は Fedora。
標準設定の分類は以下の通り。

* パッケージのインストール
* セキュリティ設定
* 標準ユーザーの作成

## Requirements

### Ansible collections

- [ansible.posix](https://docs.ansible.com/ansible/latest/collections/ansible/posix/index.html)

## ロール変数

| 変数名                                 | デフォルト値                                             | 説明                                                           |
| -------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------------- |
| linux_std_setting_packages                                                                       | [defaults/main/package.yml](./defaults/main/package.yml)を参照 |インストール対象のパッケージ群
| linux_std_setting_users                | [defaults/main/user.yml](./defaults/main/user.yml)を参照 | 作成対象のユーザーリスト                                       |
| linux_std_setting_users[n].name        | 同上 | ユーザー名                                                     |
| linux_std_setting_users[n].password    | 同上                                                        | ユーザーパスワード                                             |
| linux_std_setting_users[n].uid         | 同上                                                        | ユーザーに割り当てるUID                                        |
| linux_std_setting_users[n].enable_sudo | 同上                                                        | 特権付与フラグ                                                 |

## Playbookの例

Playbook:

```yaml
---
- name: Configure Linux standard settings
  hosts: linux_servers
  become: true
  tasks:
    - name: Import role
      ansible.builtin.import_role:
        name: linux_std_setting
```

## License

MIT

## Author Information

Kiyo Nagamine
