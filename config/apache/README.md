# Apache Configuration for protoDUNE DQM
There are differences in Apache deployment detail
and layout of configuration files on defferent flavor
of Linux. Main focus of these (simple) configuration
file is to properly deploy Django and serve static
content, in the context of the protoDUNE Data Quality
Management system.

# Permissions for wsgi.py and other components
In addition to granting permissions in the Apache configuration file, correct permissions
need to be set for the directory tree containing wsgi.py and other crucial files.
If for example the tree is contained in your home directory and it's not readable to others,
it won't work. One example (perhaps not the best) of how to make it work is to set 755 to your home dir.

On top of that, SELinux will impose it's own restriction. See:
```
getenforce
```

If it shows "Enforcing", try
```
sudo setenforce 0
```
