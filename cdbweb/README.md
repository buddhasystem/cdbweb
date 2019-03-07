# The web project folder

## Caveat
Some of the SQL here is kept for reference purposes to facilitate development, it's not used directly.

## Restoring the DB content from a snapshot (dump)
pg_restore -d myDB -U user DUMP_FILE_NAME

## DB Login
psql -U user -d myDB

-f file
