=================
django-sphinx-ext
=================

Custom Directives for use in ReST files with Sphinx, to automate creation of some documentation


++++++++++++++++++
Dependencies
++++++++++++++++++
- Python
- Django
- Sphinx
- Tabulate

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


Usage (with fields to be excluded)::

    .. form:: myapp MyFormClass
	   :exclude: ['created']

This can hide any default fields that will only clutter documentation.


If successful, a table is printed containing 
metadata for each form field.

Directly after, it checks your firm class for an err_set dict 
containing custom error messages used in the forms clean method.
these will be printed in a bulleted list.

Example Output:

	.. image:: screen/form_sample.jpg


++++++++++++++++++
viewdoc.py
++++++++++++++++++

Use Django's "reverse" function to print the url for a given urlpattern name.

Usage (Simple GET endpoint with no params)::

	.. endpoint:: 'url-name'

Usage (URL requires some parameters to be found (ex. a pk))::

	.. endpoint:: 'url-with-params'
	   :extra: {'pk': 1}

Usage (to include the HTTP method)::

	.. endpoint:: 'url-with-params'
	   :extra: {'pk': 1}
	   :method: POST

The URL will be inserted into the document inside a block-quote.
If 'method' is provided,  it will be bold and appear above the block-quote.

Example Output:

	.. image:: screen/endpoint_sample.jpg

And with a method + extra included:

	.. image:: screen/endpoint_extras_sample.jpg


