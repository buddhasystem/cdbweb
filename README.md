# CDBweb
## Motivations
The Belle II conditions DB is a critical component of its infrastructure.
Up till now user access to the content of the database was limited to
the Swagger interface, which while being functional does not provide
adequate functionality to browse, select and verify the data in the CDB,
and trace its dependencies across the DB schemas.

For that reason, the "CDBweb" application has been created which aims
to have better functionality and be more user-friendly.

## Technology
CDBweb is a Django Web app for the conditions database. At the time of
writing, it runs on Django 2.1 an Python 3.5/3.6. Since the database already
existed, we used DB introspection to create Django models which were
then finalized by hand to address the issue of foreign keys etc.

## Test service
Current testing platform for CDBweb is a VM running RH7.6:
??.sdcc.bnl.gov (contact the developer for the exact name)

## Databases
The 'default' database is used to connect to the actual CDB back-end.
A separate 'auth_db' is used to carry out Django internal operations.
This requires separate migrations e.g.

```
$ ./manage.py migrate --database=users
```






