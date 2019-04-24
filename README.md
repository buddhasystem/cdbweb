# CDBweb
## Motivations
The Belle II Conditions Database (CDB) is a critical component of its infrastructure.
As of early 2019 it was operated and monitored by means of a small suite
of command line tools. In order to make the information contained in this
database more accessible to both the database team as well as end users
it was decided to create a web application (codename "CDBweb"). It aims to
provide fast, easy and intuitive way to browse, inspect and verify the
conditions data at varying levels of detail.

## Technology

CDBweb is based on the Django web framework. At the time of writing the
versions used are Django 2.1 and Python 3.6. Since the conditions database
already existed and was in production when this development started, we
used DB introspection to create Django models. The database tables are
not managed by Django, as is often the case when one has to instrument
a legacy database.

CDBweb is not accessing the actual production instance of the CDB (PostgreSQL)
to minimize possible interference but instead is using a streaming replica
of the CDB in read-only mode.

## The service
Current platform for CDBweb is a VM running RH7.6 and hosted at BNL.


## Databases

To comply with the read-only design, CDBweb is using two separate databases:
one to access the actual data and another one to manage the Django internals,
user and group configuration and other administrative functions. Since
performance and scalability requirements for the latter database are rather
modest it is implemented as sqlite.

In order to manage the database access in this configuration a Django
feature called "database routers" is utilized.
