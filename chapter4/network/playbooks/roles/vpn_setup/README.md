# vpn_setup ロール

## 機能

拠点間VPNの設定を適用する機能を提供。

* センタールーターへのVPN接続設定
  * 指定した対向ブランチルーターとVPNトンネルを確立するための IKE,ESP,インタフェース の設定
* ブランチルーターへのVPN接続設定
  * 指定した対向センタールーターとVPNトンネルを確立するための IKE,ESP,インタフェース の設定

## 利用方法
[機能](#機能) に記載の通り、当ロールでセンタールーター、ブランチルーターのいずれもVPN設定が適用可能であるが、
それぞれの設定を同時に行うことは推奨されない。

## Requirements

### Ansible collections

- [vyos.vyos](https://docs.ansible.com/ansible/latest/collections/vyos/vyos/vyos_vlan_module.html#ansible-collections-vyos-vyos-vyos-vlan-module)

## ロール変数

| 変数名                     | デフォルト値 | 説明                                                           |
| -------------------------- | ------------ | -------------------------------------------------------------- |
| vpn_setup_router_type      | -            | 当ロールを適用する対象ルーターのタイプ('center'または'branch') |
| vpn_setup_branch_id        | -            | 拠点ID                                                         |
| vpn_setup_center_ipaddr    | -            | センタールーターのWAN側IPアドレス                              |
| vpn_setup_branch_ipaddr    | -            | ブランチルーターのWAN側IPアドレス                              |
| vpn_setup_backup_dir       | -            | コンフィグを保存するコントロールノード上のディレクトリ         |
| vpn_setup_ike_group        | IKEGroup     | IKE SA グループ名                                              |
| vpn_setup_ike_dpd_action   | restart      | IKE SA の通信断を検知した場合のアクション                      |
| vpn_setup_ike_dpd_interval | 15           | IKE SA キープアライブパケットの送信間隔(秒)                    |
| vpn_setup_ike_dpd_timeout  | 30           | IKE SA のタイムアウト値(秒)                                    |
| vpn_setup_ike_dh_group     | 2            | DH グループ番号                                                |
| vpn_setup_ike_encryption   | aes128       | IKE で利用する暗号化アルゴリズム                               |
| vpn_setup_ike_hash         | sha1         | IKE で利用する認証アルゴリズム                                 |
| vpn_setup_esp_group        | ESPGroup     | ESP グループ名                                                 |
| vpn_setup_esp_lifetime     | 3600         | ESP SA のライフタイム(秒)                                      |
| vpn_setup_esp_mode         | tunnel       | トンネルモードの指定                                           |
| vpn_setup_esp_encryption   | aes128       | ESP で利用する暗号化アルゴリズム                               |
| vpn_setup_esp_hash         | sha1         | ESP で利用する認証アルゴリズム                                 |

## Playbookの例

### センタールーターの場合

Playbook:

```yaml
---
- hosts: center_router
  gather_facts: false
  tasks:
    - name: Setup VPN center router
      ansible.builtin.import_role:
        name: vpn_setup
      vars:
        vpn_setup_router_type: center
        vpn_setup_center_ipaddr: <center route's WAN IP address>
        vpn_setup_branch_ipaddr: "{{ branch_router_ipaddr }}"
        vpn_setup_branch_id: "{{ branch_id }}"
        vpn_setup_backup_dir: ./backup_config
```

インベントリ変数 (ex. `host_vars/center_router01.yml`):

```yaml
---
branch_id: 1
branch_router_ipaddr: <branch router's WAN IP address>
```

### ブランチルーターの場合

Playbook:

```yaml
---
- hosts: branch_router
  gather_facts: false
  tasks:
    - name: Setup VPN branch router
      ansible.builtin.import_role:
        name: vpn_setup
      vars:
        vpn_setup_router_type: branch
        vpn_setup_center_ipaddr: <center route's WAN IP address>
        vpn_setup_branch_ipaddr: "{{ branch_router_ipaddr }}"
        vpn_setup_branch_id: "{{ branch_id }}"
        vpn_setup_backup_dir: ./backup_config
```

インベントリ変数 (ex. `host_vars/branch_router01.yml`):

```yaml
---
branch_id: 1
branch_router_ipaddr: <branch router's WAN IP address>
```

## License

MIT

## Author Information

Kiyo Nagamine
