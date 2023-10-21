#!/bin/bash

USERNAME=postgres
DATABASE=postgres

# Name of db
read -p "DB pod that you want to backup ": PREV_POD
read -p "DB pod that you want to apply ": NEW_POD

TODAY="$(date +%Y%m%d)"
BACKUP_FILE="backup_$TODAY.tar"

kubectl exec $PREV_POD -- pg_dump -U $USERNAME -W -F t $DATABASE > $BACKUP_FILE
echo "Database has been backed up."

# 기존 DB 삭제
kubectl exec $NEW_POD -- /bin/bash -c "
psql -U postgres -d postgres <<'EOF'
DO \$\$ DECLARE
    r RECORD;
BEGIN
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) LOOP
        EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
    END LOOP;
END \$\$;
EOF"

echo "All tables in the database have been dropped."

# Backup 진행
kubectl cp ./$BACKUP_FILE $NEW_POD:/$BACKUP_FILE
kubectl exec $NEW_POD -- bash -c "pg_restore -U postgres -d postgres /$BACKUP_FILE"
echo "Database has been restored."