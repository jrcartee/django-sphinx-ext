=================
django-sphinx-ext
=================

Custom Directives for use in ReST files with Sphinx, to automate creation of some documentation.
Contains the following directives:
	- pyexec_ -- executes arbitrary python code, and redirects stdout to your generated doc
	- formdoc_ -- builds a table describing all your django form's fields (works for django-rest-framework serializers too!)
	- viewdoc_ -- uses django's reverse to print the url for each view, using its name given in your urls.py files

.. _pyexec: https://github.com/jrcartee/django-sphinx-ext/blob/master/docs/pyexec.rst
.. _formdoc: https://github.com/jrcartee/django-sphinx-ext/blob/master/docs/formdoc.rst
.. _viewdoc: https://github.com/jrcartee/django-sphinx-ext/blob/master/docs/viewdoc.rst

++++++++++++++++++
Dependencies
++++++++++++++++++
- Python 2.7
- Django 1.6
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
