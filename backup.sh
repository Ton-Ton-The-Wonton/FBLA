#!/bin/bash
BACKUP_CMD="sqlite3 data.db .dump > $BACKUP_DIR/data.sql"
(crontab -l; echo "*/30 * * * * ${BACKUP_CMD}") | sort -u | crontab -