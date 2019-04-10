# The web project folder

## Caveats
* The "static" directory is a replica of what needs to be under /var/www or a similar location.
* The SQL macros in the "sql" is kept for reference purposes and to facilitate development, this code not used in the web application directly.

## Restoring the DB content from a snapshot (dump)
pg_restore -d myDB -U user DUMP_FILE_NAME

## DB Login
psql -U user -d myDB

-f file

## Restart the service
sudo systemctl restart httpd.service

## Pulling files from the RACF ftp server
scp user@rftpexp.rhic.bnl.gov:foo foo

