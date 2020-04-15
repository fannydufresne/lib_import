.. lib_import documentation master file, created by
   sphinx-quickstart on Tue Apr 14 18:16:20 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

lib_import
==================

lib_import is a Django library for importing data (file -> database).
It is based on django-import-export


Two possible types of import are defined :

- Create only
   New objects are created, but existing objects are not updated, and
   corresponding rows are skipped.

- Create and update
   New objects are created, existing objects are updated.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules/views.rst
   modules/resources.rst
   modules/exceptions.rst
   modules/forms.rst



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
