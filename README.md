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
CDBWEB is a Django Web app for the conditions database. At the time of
writing, it runs on Django 2.1 an Python 3.5. Since the database already
existed, we used DB introspection to create Django models which were
then finalized by hand to address the issue of foreign keys etc.


