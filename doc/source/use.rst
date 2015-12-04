..  _cygenja_use:

=========================================================
Use
=========================================================


The `Generator` class
------------------------

The :class:`Generator` class is the main class of the :program:`cygenja` library. It is also the only 
class you needs to interact with. It's constructor is really simple:

..  code-block:: python

    from cygenja.generator import Generator
    ...
    
    logger = ...
    engine = Generator('root_directory', logger, True)

You give a *root* directory, a *logger* and decides if *warnings* must raise `Exception`\s or not. We describe the root directory a little further in :ref:`root_directory` and develop the two other arguments
in the next corresponding subsections. 

Logging
"""""""""

A logging engine *can* be used but is not mandatory. If you don't want to log :program:`cygenja`\'s behavior, simply pass `None` for the logger argument in the constructor. The logging engine is 
an object from Python's `logging library <https://docs.python.org/2/library/logging.html>`_.

..  code-block:: python

    from cygenja.generator import Generator
    import logging
    
    logger = logging.getLogger('Logger name') 
    engine = Generator('root_directory', logger, True)

Three message logging helpers are provided:

..  code-block:: python

    def log_info(self, msg)
    def log_warning(self, msg)
    def log_error(self, msg)
    
Their names and signatures are quite self-explanatory. 


Raising exceptions on *Warnings*
""""""""""""""""""""""""""""""""""

Errors **always** trigger `RuntimeError`\s while warnings may or may not trigger `RuntimeError`\s. To raise exceptions on warnings, set the ``raise_exception_on_warning`` to ``True`` in the 
constructor:

..  code-block:: python

    engine = Generator('root_directory', logger=logger, raise_exception_on_warning=True)

By default, ``raise_exception_on_warning`` is ``False``.


..  _root_directory:

The *root* directory
-----------------------

The root directory is really the main working directory: all file generations can **only** be done inside **subdirectories** of this directory. 

This is so important, we need a warning:

..  warning::

    File generations can **only** be done inside **subdirectories** of the *root* directory.
    
This directory is given a first parameter of :class:`Generator`\'s constructor
and can be absolute or relative. At any moment, you can retrieve this directory as an absolute path:

..  code-block:: python

    engine = Generator('root_directory', ...)
    
    absolute_root_directory = engine.root_directory()

Filters
--------

Filters are simply :program:`Jinja2` `filters <http://jinja.pocoo.org/docs/dev/templates/#filters>`_. These filters are *registered*:

..  code-block:: python

    def my_jinja2_filter(filter_argument):
        ...
        return filter_result
        
    engine = Generator(...)
    engine.register_filter('my_filter_name', my_jinja2_filter)

where ``'my_filter_name'`` if the name of the filter used inside your :program:`Jinja2` template files and ``my_jinja2_filter`` is a reference to the actual filter.

The signature of ``register_filter`` is:

..  code-block:: python
    
    register_filter(self, filter_name, filter_ref, force=False)

allowing you to register a new filter under an already existing filter name. If you keep ``force`` set to ``False``, a warning is triggered each time you try to register a 
new filter under an already existing filter name and this **new** filter is disregarded. 

You also can register several filters at once with a dictonary of filters:

..  code-block:: python

    engine = Generator(...)
    filters = { 'f1' : filter1,
                'f2' : filter2}
                
    engine.register_filters(filters, force=False)
    
At any time, you can list the registered filters: 

..  code-block:: python

    engine = Generator(...)
    print engine.filters_list()


This list also includes predefined :program:`Jinja2` filters (see `builtin filter <http://jinja.pocoo.org/docs/dev/templates/#builtin-filters>`_).
If you only want the filters you registered, invoke:

..  code-block:: python

    engine.registered_filters_list()

File extensions
----------------

:program:`cygenja` uses a correspondance table between template files and generated files. This table defines a correspondance between file *extensions*. For instance, to have `*.cpd` templates generate  `*.pxd` files:

..  code-block:: python

    engine = Generator(...)
    engine.register_extension(`.cpd`, `.pxd`)
    
Again, we use a ``force`` switch to force the redefinition of such a correspondance. By default, this switch is set to ``False`` and if you try to redefine an association with a given template extension, you will 
trigger a warning and this new correspondance will be disregarded.
    
You can use a ``dict`` to register several extensions at once:

..  code-block:: python

    engine = Generator(...)
    ext_correspondance = { '.cpd' : '.pxd',
                           '.cpx' : 'pyx'}
    engine.register_extensions(ext_correspondance, force=False):

As with filters, you can retrieve the registered extensions:

..  code-block:: python

    engine.registered_extensions_list()

Actions
----------

File generation
-----------------



