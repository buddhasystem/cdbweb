# Configuration files specific to Apache 2.4 on CentOS

Confoguration files in this directory are kept as examples
helpful in confguring the CDBweb service, coming from
a separate web application. They are not
currently useable "as is".

At the time of writing, all is kept in one directory.
These files can be used to overwrite the defaults in
the standard Apache installation.

For example:
```
$ ls /etc/httpd/
conf  conf.d  conf.modules.d  logs  modules  run
$ ls /etc/httpd/conf.d/
autoindex.conf  django.conf  php.conf  README  userdir.conf  welcome.conf
```

/etc/httpd/conf - no substabtial changes

/etc/httpd/conf.d - django.conf crucial
* contains a reference to "settings.py"

/etc/httpd/conf.modules.d/00-base.conf - must contain an entry for wsgi