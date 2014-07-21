=================
django-sphinx-ext
=================

Custom Directives for use in ReST files with Sphinx, to automate creation of some documentation


++++++++++++++++++
Setup
++++++++++++++++++

In your Sphinx project's conf.py::

	sys.path.insert(0, os.path.abspath('/path/to/your/django_project/'))
	sys.path.insert(0, os.path.abspath('/path/to/this/cloned/repo/'))


	extensions = [
	    'pyexec',
	    'viewdoc',
	    'formdoc'
	]


++++++++++++++++++
pyexec.py
++++++++++++++++++

Execute arbitrary python code in a ReST document.

Usage::
	.. exec:: 
	   print "your python code here!"
	   print "even on multiple lines"

This inserts any output that goes to stdout into the ReST document
prior to the interpretation by Sphinx. 

Code for pyexec module was found from this stackoverflow answer:
	http://stackoverflow.com/a/18143318
Credit goes to StackOverflow user: 
	http://stackoverflow.com/users/839411/alex-forencich


++++++++++++++++++
formdoc.py
++++++++++++++++++

Auto-generate documentation for a Django Form Class.

Usage::
	.. form:: myapp MyFormClass

This attempts to import MyFormClass from myapp.forms.

If successful, a table is printed containing 
metadata for each form field including:
	- required
	- max_length
	- min_value
	- max_value
	- help_text

Directly after, it checks your firm class for an err_set dict 
containing custom error messages used in the forms clean method.
these will be printed in a bulleted list.


++++++++++++++++++
viewdoc.py
++++++++++++++++++

Use Django's "reverse" function to print the url for a given urlpattern name.

Usage::
	.. endpoint:: 'url-name'

	If the url requires some parameters to be found (ex. a pk):

	.. endpoint:: 'url-with-params'
	   :extra: {'pk': 1}

The URL will be inserted into the document inside a block-quote.