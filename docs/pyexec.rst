++++++++++++++++++
pyexec.py
++++++++++++++++++

Executes arbitrary python code and redirects stdout to your documentation.

Usage::

    .. exec::
       print "your python code here!"
       print "even on multiple lines"

This inserts any output that goes to stdout into the ReST document
prior to the interpretation by Sphinx. This means the output may include ReST formatting,
and it will be parsed and converted in the final output.

|

Code for pyexec module was found from this stackoverflow answer:
    http://stackoverflow.com/a/18143318
Credit goes to StackOverflow user:
    http://stackoverflow.com/users/839411/alex-forencich