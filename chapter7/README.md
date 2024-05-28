# 第7章　ハンズオン補足資料
# 本READMEは第7章の補足資料です。内容は以下の通りとなります。
1. [本章の訂正事項](#1-本章の訂正事項)
2. [「7.2 AWXのインストール - WindowsホストでのAWXの構築手順」](#2-72-awxのインストール---windowsホストでのawxの構築手順)
3. [「7.6 "作業の承認と通知" の補足事項」](#3-76-作業の承認と通知-の補足事項)
4. [「7.7 "実行ログの適切な管理" の環境構築手順」](#4-77-実行ログの適切な管理-の環境構築手順)

## 1. 本章の訂正事項
はじめに、本章の一部を以下に訂正させていただきます。
- 7.4.4 実行環境の登録 表7.10の設定項目「プロジェクト」は不要
- 7.6.1 セキュリティアップデートジョブの作成　表7.16および表7.17の設定項目「実行環境」は、「ハンズオンの事前準備」で作成した実行環境名「Ansible book 07 Custom EE」に訂正

## 2. 「7.2 AWXのインストール - WindowsホストでのAWXの構築手順」
本章の検証環境としてWindowsホストをご利用される場合は、こちらの構築手順をご参考ください。

### ネットワークトポロジー図:
```
-----------+----------- <NAT network>
           |
           |
     [eth0]|
    Virtual Machine
           |[eth1]
           |
           |.4
-----------+----------- <private network:192.168.57.0/24>
```

### 構築手順

`labs` リポジトリにチェックアウトする:
```shell
$ git clone https://github.com/ansible-bookground/labs.git
$ cd lab/vagrant/awx_fedora
```

[vagrant-vbguest](https://github.com/dotless-de/vagrant-vbguest) プラグインをインストールする。

```shell
$ vagrant plugin install vagrant-vbguest
```

[vagrant-hostsupdater](https://github.com/agiledivider/vagrant-hostsupdater) プラグインをインストールする。

```shell
$ vagrant plugin install vagrant-hostsupdater
```

Vagrant upコマンドで仮想マシンを起動する:
```shell
$ vagrant up
```

### vagrant sshで仮想マシンにログイン後、minikubeを起動する:
```shell
$ vagrant ssh
[vagrant@awx ~]$ minikube start --cpus='3' --memory='6g'
😄  minikube v1.32.0 on Redhat 9.3 (vbox/amd64)
✨  Automatically selected the podman driver. Other choices: ssh, none
📌  Using Podman driver with root privileges
👍  Starting control plane node minikube in cluster minikube
🚜  Pulling base image ...
💾  Downloading Kubernetes v1.28.3 preload ...
    > gcr.io/k8s-minikube/kicbase...:  453.90 MiB / 453.90 MiB  100.00% 9.45 Mi
    > preloaded-images-k8s-v18-v1...:  403.35 MiB / 403.35 MiB  100.00% 7.82 Mi
E0130 05:20:15.113290   11324 cache.go:189] Error downloading kic artifacts:  not yet implemented, see issue #8426
🔥  Creating podman container (CPUs=2, Memory=4096MB) ...
🐳  Preparing Kubernetes v1.28.3 on Docker 24.0.7 ...
    ▪ Generating certificates and keys ...
    ▪ Booting up control plane ...
    ▪ Configuring RBAC rules ...
🔗  Configuring bridge CNI (Container Networking Interface) ...
🔎  Verifying Kubernetes components...
    ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
🌟  Enabled addons: default-storageclass, storage-provisioner
🏄  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
[vagrant@awx ~]$
```

### minikubeを利用して、AWXをデプロイする

Stage1: work/awx/stage1/配下のマニフェストファイルをapplyする.

```shell
[vagrant@awx ~]$ kubectl apply -k work/awx/stage1/
namespace/awx created
customresourcedefinition.apiextensions.k8s.io/awxbackups.awx.ansible.com created
customresourcedefinition.apiextensions.k8s.io/awxrestores.awx.ansible.com created
customresourcedefinition.apiextensions.k8s.io/awxs.awx.ansible.com created
serviceaccount/awx-operator-controller-manager created
role.rbac.authorization.k8s.io/awx-operator-awx-manager-role created
role.rbac.authorization.k8s.io/awx-operator-leader-election-role created
clusterrole.rbac.authorization.k8s.io/awx-operator-metrics-reader created
clusterrole.rbac.authorization.k8s.io/awx-operator-proxy-role created
rolebinding.rbac.authorization.k8s.io/awx-operator-awx-manager-rolebinding created
rolebinding.rbac.authorization.k8s.io/awx-operator-leader-election-rolebinding created
clusterrolebinding.rbac.authorization.k8s.io/awx-operator-proxy-rolebinding created
configmap/awx-operator-awx-manager-config created
service/awx-operator-controller-manager-metrics-service created
deployment.apps/awx-operator-controller-manager created
[vagrant@awx ~]$
```

以下のように、awx-operator-controller-manager podのステータスがRunningとなるのを確認する。
※ステータスが変わらない場合は何回かコマンドを実行してみてください。
```shell
[vagrant@awx ~]$ kubectl get pods -n awx
NAME                                               READY   STATUS    RESTARTS   AGE
awx-operator-controller-manager-775bd7b75d-s8hj4   2/2     Running   0          67s
```

Stage2: AWX アプリケーションをデプロイする.
```shell
[vagrant@awx ~]$ kubectl apply -k work/awx/stage2/
deployment.apps/awx-operator-controller-manager created
[vagrant@awx ~]$ kubectl get pods -n awx
NAME                                               READY   STATUS    RESTARTS   AGE
awx-operator-controller-manager-775bd7b75d-s8hj4   2/2     Running   0          67s
[vagrant@awx ~]$ kubectl apply -k work/awx/stage2/
namespace/awx unchanged
customresourcedefinition.apiextensions.k8s.io/awxbackups.awx.ansible.com unchanged
customresourcedefinition.apiextensions.k8s.io/awxrestores.awx.ansible.com unchanged
customresourcedefinition.apiextensions.k8s.io/awxs.awx.ansible.com unchanged
serviceaccount/awx-operator-controller-manager unchanged
role.rbac.authorization.k8s.io/awx-operator-awx-manager-role configured
role.rbac.authorization.k8s.io/awx-operator-leader-election-role unchanged
clusterrole.rbac.authorization.k8s.io/awx-operator-metrics-reader unchanged
clusterrole.rbac.authorization.k8s.io/awx-operator-proxy-role unchanged
rolebinding.rbac.authorization.k8s.io/awx-operator-awx-manager-rolebinding unchanged
rolebinding.rbac.authorization.k8s.io/awx-operator-leader-election-rolebinding unchanged
clusterrolebinding.rbac.authorization.k8s.io/awx-operator-proxy-rolebinding unchanged
configmap/awx-operator-awx-manager-config unchanged
service/awx-operator-controller-manager-metrics-service unchanged
deployment.apps/awx-operator-controller-manager unchanged
awx.awx.ansible.com/awx-app created
```

各Pod(awx-app-postgres、awx-app-task、awx-app-web、awx-operator-controller-manager)のステータスがRunningとなるのを確認する。
```shell
[vagrant@awx ~]$ kubectl get pods -n awx
NAME                                               READY   STATUS    RESTARTS   AGE
awx-app-postgres-13-0                              1/1     Running   0          2m12s
awx-app-task-98f94bd49-r5ngf                       4/4     Running   0          99s
awx-app-web-565f4dbc89-84bz4                       3/3     Running   0          8s
awx-operator-controller-manager-775bd7b75d-s8hj4   2/2     Running   0          3m57s
[vagrant@awx ~]$ kubectl get svc -n awx
NAME                                              TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
awx-app-postgres-13                               ClusterIP   None            <none>        5432/TCP       2m55s
awx-app-service                                   NodePort    10.102.21.232   <none>        80:30834/TCP   2m24s
awx-operator-controller-manager-metrics-service   ClusterIP   10.99.42.221    <none>        8443/TCP       4m40s
```

AWXアプリケーションのデプロイが完了したら、以下のコマンドで、起動されたAWXのURLを確認する:
```shell
[vagrant@awx ~]$ minikube service awx-app-service -n awx --url
http://192.168.49.2:30834
```

AWXのadminユーザのパスワードを確認する:
```shell
$ kubectl get secret -n awx awx-app-admin-password -o jsonpath="{.data.password}" | base64 --decode ; echo
```

最後に、WindowsホストのPowershell(もしくはコマンドプロンプト)で以下のコマンドを実行して、AWXにアクセスするためのルーティングを設定する。

```shell
> route add 192.168.49.0 mask 255.255.255.0 192.168.57.4
```

その後、上記のステップで確認したAWXのURL(本READMEの例の場合は http://192.168.49.2:30834)にWindowsホストのブラウザから接続する。

<br>

## 3. 「7.6 "作業の承認と通知" の補足事項」
本ハンズオンでは、実際にマネージドノードに対してSSHログインしてタスクを実行するワークフロージョブテンプレートを作成します。
この時、SSHのログインユーザはマネージドノードでsudoユーザーへの権限昇格を行います。
ご利用のマネージドノード内でsudoユーザーへの権限昇格時、パスワードが必要となる場合、リスト7.1「検証環境のホスト情報」の箇所でインベントリ変数を定義してください。
例えば、sudo権限に昇格する際に利用するパスワードが`changeme`の場合、当該箇所に以下のように定義します。

```
---
ansible_become_pass: changeme
```

## 4. 「7.7 "実行ログの適切な管理" の環境構築手順」
ここでは、検証用のELK(Elasticsearch, Logstash, Kibana)を構築するための最低限の設定のみを記載しています。各種設定の詳細や他の設定項目については、それぞれの公式ドキュメントをご参考ください。

### Elasticsearchの構築手順
以下の手順はすべて、Ansibleコントロールノード以外の任意のサーバーで実行してください。なお、利用するOSはRHEL/CentOS/Fedoraを想定しています。

1. dnf リポジトリを構成します。`/etc/yum.repos.d/elastic.repo`ファイルを以下の内容で作成して保存してください。
```
[elasticsearch]
name=Elastic repository for 8.x packages
baseurl=https://artifacts.elastic.co/packages/8.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=1
autorefresh=1
type=rpm-md
```

2. Elasticsearchのパッケージをインストールします。

```
$ sudo yum -y install elasticsearch
$ sudo rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch
```

<br>
<br>

3.　`/etc/elasticsearch/elasticsearch.yml`ファイルをバックアップ後、`/etc/elasticsearch/elasticsearch.yml`ファイルを作成してください。
ここでは、`/etc/elasticsearch/elasticsearch.yml`ファイルを`/etc/elasticsearch/elasticsearch.yml.bk`ファイルとして保存しています。
```
$ sudo mv /etc/elasticsearch/elasticsearch.yml /etc/elasticsearch/elasticsearch.yml.bk
```
`/etc/elasticsearch/elasticsearch.yml`ファイルを作成し、以下の内容で保存してください。
```
# ======================== Elasticsearch Configuration =========================
#
# NOTE: Elasticsearch comes with reasonable defaults for most settings.
#       Before you set out to tweak and tune the configuration, make sure you
#       understand what are you trying to accomplish and the consequences.
#
# The primary way of configuring a node is via this file. This template lists
# the most important settings you may want to configure for a production cluster.
#
# Please consult the documentation for further information on configuration options:
# https://www.elastic.co/guide/en/elasticsearch/reference/index.html
#
# ---------------------------------- Cluster -----------------------------------
#
# Use a descriptive name for your cluster:
#
#cluster.name: my-application
cluster.name: cluster01
discovery.type: single-node

# ------------------------------------ Node ------------------------------------
#
# Use a descriptive name for the node:
#
#node.name: node-1
node.name: node01
#ansible.example.com

# Add custom attributes to the node:
#
#node.attr.rack: r1
#
# ----------------------------------- Paths ------------------------------------
#
# Path to directory where to store the data (separate multiple locations by comma):
#
path.data: /var/lib/elasticsearch
#
# Path to log files:
#
path.logs: /var/log/elasticsearch
#
# ----------------------------------- Memory -----------------------------------
#
# Lock the memory on startup:
#
#bootstrap.memory_lock: true
#
# Make sure that the heap size is set to about half the memory available
# on the system and that the owner of the process is allowed to use this
# limit.
#
# Elasticsearch performs poorly when the system is swapping the memory.
#
# ---------------------------------- Network -----------------------------------
#
# By default Elasticsearch is only accessible on localhost. Set a different
# address here to expose this node on the network:
network.host: 0.0.0.0

# By default Elasticsearch listens for HTTP traffic on the first free port it
# finds starting at 9200. Set a specific HTTP port here:
#
#http.port: 9200
#
# For more information, consult the network module documentation.
#
# --------------------------------- Discovery ----------------------------------
#
# Pass an initial list of hosts to perform discovery when this node is started:
# The default list of hosts is ["127.0.0.1", "[::1]"]
#
#discovery.seed_hosts: ["host1", "host2"]
#
# Bootstrap the cluster using an initial set of master-eligible nodes:
#
#cluster.initial_master_nodes: ["node-1", "node-2"]
#cluster.initial_master_nodes: ["node01"]
# For more information, consult the discovery and cluster formation module documentation.
#
# ---------------------------------- Various -----------------------------------
#
# Allow wildcard deletion of indices:
#
#action.destructive_requires_name: false

#----------------------- BEGIN SECURITY AUTO CONFIGURATION -----------------------
#
# The following settings, TLS certificates, and keys have been automatically      
# generated to configure Elasticsearch security features on 19-02-2024 03:33:24
#
# --------------------------------------------------------------------------------

# Enable security features
xpack.security.enabled: false

xpack.security.enrollment.enabled: false

# Enable encryption for HTTP API client connections, such as Kibana, Logstash, and Agents
xpack.security.http.ssl:
  enabled: false
  keystore.path: certs/http.p12

# Enable encryption and mutual authentication between cluster nodes
xpack.security.transport.ssl:
  enabled: false
  verification_mode: certificate
  keystore.path: certs/transport.p12
  truststore.path: certs/transport.p12
# Create a new cluster with the current node only
# Additional nodes can still join the cluster later
#cluster.initial_master_nodes: ["ansible.example.com"]

# Allow HTTP API connections from anywhere
# Connections are encrypted and require user authentication
http.host: 0.0.0.0

# Allow other nodes to join the cluster from anywhere
# Connections are encrypted and mutually authenticated
#transport.host: 0.0.0.0

#----------------------- END SECURITY AUTO CONFIGURATION -------------------------

```

4. `elasticsearch.service`を起動します。

```
$ sudo systemctl restart elasticsearch 
```


<br>


### Kibanaの構築手順

1. Kibanaパッケージをインストールしてください。
```
$ sudo dnf install kibana
```

2. `/etc/kibana/kibana.yml`ファイルをバックアップし、`/etc/kibana/kibana.yml`ファイルを編集します。
まずはバックアップのため、`/etc/kibana/kibana.yml`ファイルを`/etc/kibana/kibana.yml.bk`として保存します。
```
$ sudo mv /etc/kibana/kibana.yml /etc/kibana/kibana.yml.bk
```

/etc/kibana/kibana.ymlファイルを作成し、以下の内容に編集します。`192.168.57.3`は実際のサーバーのIPアドレスに合わせてください。
```
# For more configuration options see the configuration guide for Kibana in
# https://www.elastic.co/guide/index.html

# =================== System: Kibana Server ===================
# Kibana is served by a back end server. This setting specifies the port to use.
#server.port: 5601

# Specifies the address to which the Kibana server will bind. IP addresses and host names are both valid values.
# The default is 'localhost', which usually means remote machines will not be able to connect.
# To allow connections from remote users, set this parameter to a non-loopback address.
#server.host: "localhost"
server.host: "192.168.57.3"

# Enables you to specify a path to mount Kibana at if you are running behind a proxy.
# Use the `server.rewriteBasePath` setting to tell Kibana if it should remove the basePath
# from requests it receives, and to prevent a deprecation warning at startup.
# This setting cannot end in a slash.
#server.basePath: ""

# Specifies whether Kibana should rewrite requests that are prefixed with
# `server.basePath` or require that they are rewritten by your reverse proxy.
# Defaults to `false`.
#server.rewriteBasePath: false

# Specifies the public URL at which Kibana is available for end users. If
# `server.basePath` is configured this URL should end with the same basePath.
#server.publicBaseUrl: ""

# The maximum payload size in bytes for incoming server requests.
#server.maxPayload: 1048576

# The Kibana server's name. This is used for display purposes.
#server.name: "your-hostname"
server.name: "localhost"

# =================== System: Kibana Server (Optional) ===================
# Enables SSL and paths to the PEM-format SSL certificate and SSL key files, respectively.
# These settings enable SSL for outgoing requests from the Kibana server to the browser.
#server.ssl.enabled: false
#server.ssl.certificate: /path/to/your/server.crt
#server.ssl.key: /path/to/your/server.key

# =================== System: Elasticsearch ===================
# The URLs of the Elasticsearch instances to use for all your queries.
#elasticsearch.hosts: ["http://localhost:9200"]
elasticsearch.hosts: ["http://192.168.57.3:9200"]

# If your Elasticsearch is protected with basic authentication, these settings provide
# the username and password that the Kibana server uses to perform maintenance on the Kibana
# index at startup. Your Kibana users still need to authenticate with Elasticsearch, which
# is proxied through the Kibana server.
#elasticsearch.username: "kibana_system"
#elasticsearch.password: "pass"

# Kibana can also authenticate to Elasticsearch via "service account tokens".
# Service account tokens are Bearer style tokens that replace the traditional username/password based configuration.
# Use this token instead of a username/password.
# elasticsearch.serviceAccountToken: "my_token"

# Time in milliseconds to wait for Elasticsearch to respond to pings. Defaults to the value of
# the elasticsearch.requestTimeout setting.
#elasticsearch.pingTimeout: 1500

# Time in milliseconds to wait for responses from the back end or Elasticsearch. This value
# must be a positive integer.
#elasticsearch.requestTimeout: 30000

# The maximum number of sockets that can be used for communications with elasticsearch.
# Defaults to `Infinity`.
#elasticsearch.maxSockets: 1024

# Specifies whether Kibana should use compression for communications with elasticsearch
# Defaults to `false`.
#elasticsearch.compression: false

# List of Kibana client-side headers to send to Elasticsearch. To send *no* client-side
# headers, set this value to [] (an empty list).
#elasticsearch.requestHeadersWhitelist: [ authorization ]

# Header names and values that are sent to Elasticsearch. Any custom headers cannot be overwritten
# by client-side headers, regardless of the elasticsearch.requestHeadersWhitelist configuration.
#elasticsearch.customHeaders: {}

# Time in milliseconds for Elasticsearch to wait for responses from shards. Set to 0 to disable.
#elasticsearch.shardTimeout: 30000

# =================== System: Elasticsearch (Optional) ===================
# These files are used to verify the identity of Kibana to Elasticsearch and are required when
# xpack.security.http.ssl.client_authentication in Elasticsearch is set to required.
#elasticsearch.ssl.certificate: /path/to/your/client.crt
#elasticsearch.ssl.key: /path/to/your/client.key

# Enables you to specify a path to the PEM file for the certificate
# authority for your Elasticsearch instance.
#elasticsearch.ssl.certificateAuthorities: [ "/path/to/your/CA.pem" ]

# To disregard the validity of SSL certificates, change this setting's value to 'none'.
#elasticsearch.ssl.verificationMode: full

# =================== System: Logging ===================
# Set the value of this setting to off to suppress all logging output, or to debug to log everything. Defaults to 'info'
#logging.root.level: debug

# Enables you to specify a file where Kibana stores log output.
logging:
  appenders:
    file:
      type: file
      fileName: /var/log/kibana/kibana.log
      layout:
        type: json
  root:
    appenders:
      - default
      - file
#  layout:
#    type: json

# Logs queries sent to Elasticsearch.
#logging.loggers:
#  - name: elasticsearch.query
#    level: debug

# Logs http responses.
#logging.loggers:
#  - name: http.server.response
#    level: debug

# Logs system usage information.
#logging.loggers:
#  - name: metrics.ops
#    level: debug

# =================== System: Other ===================
# The path where Kibana stores persistent data not saved in Elasticsearch. Defaults to data
#path.data: data

# Specifies the path where Kibana creates the process ID file.
pid.file: /run/kibana/kibana.pid

# Set the interval in milliseconds to sample system and process performance
# metrics. Minimum is 100ms. Defaults to 5000ms.
#ops.interval: 5000

# Specifies locale to be used for all localizable strings, dates and number formats.
# Supported languages are the following: English (default) "en", Chinese "zh-CN", Japanese "ja-JP", French "fr-FR".
#i18n.locale: "en"

# =================== Frequently used (Optional)===================

# =================== Saved Objects: Migrations ===================
# Saved object migrations run at startup. If you run into migration-related issues, you might need to adjust these settings.

# The number of documents migrated at a time.
# If Kibana can't start up or upgrade due to an Elasticsearch `circuit_breaking_exception`,
# use a smaller batchSize value to reduce the memory pressure. Defaults to 1000 objects per batch.
#migrations.batchSize: 1000

# The maximum payload size for indexing batches of upgraded saved objects.
# To avoid migrations failing due to a 413 Request Entity Too Large response from Elasticsearch.
# This value should be lower than or equal to your Elasticsearch cluster’s `http.max_content_length`
# configuration option. Default: 100mb
#migrations.maxBatchSizeBytes: 100mb

# The number of times to retry temporary migration failures. Increase the setting
# if migrations fail frequently with a message such as `Unable to complete the [...] step after
# 15 attempts, terminating`. Defaults to 15
#migrations.retryAttempts: 15

# =================== Search Autocomplete ===================
# Time in milliseconds to wait for autocomplete suggestions from Elasticsearch.
# This value must be a whole number greater than zero. Defaults to 1000ms
#unifiedSearch.autocomplete.valueSuggestions.timeout: 1000

# Maximum number of documents loaded by each shard to generate autocomplete suggestions.
# This value must be a whole number greater than zero. Defaults to 100_000
#unifiedSearch.autocomplete.valueSuggestions.terminateAfter: 100000
```

3. `kibana.service`を起動します。
```
$ sudo systemctl start kibana
```

<br>

### Logstashの構築手順

1. Logstashパッケージをインストールしてください。
```
$ sudo dnf install logstash
```

2. `/etc/logstash/conf.d/logstash.conf`ファイルを以下の内容で作成し保存します。設定ファイル内の`192.168.57.3`は実際にLogstashをインストールするノードのIPアドレスに合わせてください。

```
input {
    http {
        port => 5140
    }
}
filter {
   json {
       source => "message"
   }
}
output {
    elasticsearch {
        hosts => "192.168.57.3"
        index => "awx"
    }
}

```

3. `logstash.service`を起動します。

```
$ sudo systemctl start logstash
```

最後に、ELKのダッシュボードとなるkibanaのアドレス`http://{ip_address}:{port}/`にウェブブラウザからアクセスしてください。
本READMEの設定ファイルの場合、アクセス先は以下のようになります。
```
http://192.168.57.3:5601/
```


