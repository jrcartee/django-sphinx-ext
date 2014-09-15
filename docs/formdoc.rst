++++++++++++++++++
The FormDoc Directive
++++++++++++++++++

Auto-generate documentation for a Django Form or Django-Rest-Framework Serializer Class.

|

Simple Usage ::

    .. form:: myapp.forms MyFormClass

This attempts to import MyFormClass from myapp.forms, and build a table describing the fields.

|

The **exclude** option::

    .. form:: myapp.forms MyFormClass
       :exclude: ['created', 'creator']


This option is used to hide specific fields from the output.

    *Expects a syntactically correct python list*

|

The **error_dict** option::

    .. form:: myapp.forms MyFormClass
       :error_dict: ERRORS

This option looks for a dictionary named 'ERRORS' on the form class.
If found, the dictionary values will be printed in a separate box
below the table.

|

The **prep_kwargs** and **kwargs** options::

    .. form:: myapp.forms MyFormClass
       :kwargs: {'users': None}

An instance of the form is created, and the 'fields' dictionary is used to populate the table.
This allows capturing of any changes which occur in the __init__ method.
The **kwargs** option will use the provided dict to populate the form's kwargs on instantiation.

    *Expects a syntactically correct python dictionary*

If some extra code is required in order to populate kwargs,
it can be handed in using the **prep_kwargs** option.
This may be on multiple lines and will be executed before handing kwargs to the form's constructor.
::
    .. form:: myapp.forms MyFormClass
       :prep_kwargs:
           from accounts.models import User
           user = User.objects.get(username="TestUser")
       :kwargs: {'user': user}

|

Example Output:

    .. image:: screens/form_sample.jpg