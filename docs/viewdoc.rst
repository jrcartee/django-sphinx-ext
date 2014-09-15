++++++++++++++++++
viewdoc.py
++++++++++++++++++

Uses Django's "reverse" function to print the url for a given urlpattern name.

Usage::

    .. endpoint:: 'url-name'

- The URL will be inserted into the document inside a block-quote.

|

The **method** option::

    .. endpoint:: 'url-name'
       :method: POST

- Provided method will be bolded and appear above the block-quote.

|

The **extra** option::

    .. endpoint:: 'url-with-params'
       :extra: {'pk': 1}

- Django's 'reverse' may require extra kwargs to find your url. This option covers that use-case.

|

Example Output:

    .. image:: screens/view_sample.jpg

And where extra is required you might get something like this:

    .. image:: screens/view_extra_option.jpg


