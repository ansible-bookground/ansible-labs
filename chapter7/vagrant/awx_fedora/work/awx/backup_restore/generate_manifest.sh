#!/bin/sh

UUID=`uuidgen`
BASE_DIR="./manifest"

mkdir -p $BASE_DIR/$UUID

cat <<EOF > $BASE_DIR/$UUID/backup.yaml
---
apiVersion: awx.ansible.com/v1beta1
kind: AWXBackup
metadata:
  name: awxbackup-$UUID
  namespace: awx
spec:
  deployment_name: awx-app
  backup_pvc: awxbackup-pvc
  no_log: false
EOF

echo "Backup manifest:$BASE_DIR/$UUID/backup.yaml has been created."

cat <<EOF > $BASE_DIR/$UUID/restore.yaml
---
apiVersion: awx.ansible.com/v1beta1
kind: AWXRestore
metadata:
  name: awxrestore-$UUID
  namespace: awx
spec:
  deployment_name: awx-app
  backup_name: awxbackup-$UUID
  backup_pvc: awxbackup-pvc
  force_drop_db: true
  no_log: false
EOF

echo "Restore manifest:$BASE_DIR/$UUID/restore.yaml has been created."

# EOF
