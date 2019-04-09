# The web project folder

## Caveats
* Some of the SQL here is kept for reference purposes to facilitate development, it's not used directly.
* the "static" directory is a replica of what needs to be under /var/www or a similar location

## Restoring the DB content from a snapshot (dump)
pg_restore -d myDB -U user DUMP_FILE_NAME

## DB Login
psql -U user -d myDB

-f file

## Restart the service
sudo systemctl restart httpd.service

## Pulling files from the RACF ftp server
scp user@rftpexp.rhic.bnl.gov:foo foo

