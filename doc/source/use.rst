..  _cygenja_use:

=========================================================
Use
=========================================================

We describe briefly the use of :program:`cygenja`. Basically, you register some filters, file extensions and actions before trigger the translation by invoking the ``generate()`` method.
In the :ref:`cygenja_examples` section, you can see :program:`cygenja` in action as we detail its use to generate the `CySparse <https://github.com/PythonOptimizers/cysparse>`_ library.

..  _generator_class:

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

:program:`cygenja` **only** uses the following :program:`Jinja2` environment:

..  code-block:: python

    self.__jinja2_environment = Environment(
            autoescape=False,
            loader=FileSystemLoader('/'), # we use absolute filenames
            trim_blocks=False,
            variable_start_string='@',
            variable_end_string='@')

If you want, you can change this in the source code.

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


Patterns
---------

There are only **two** types of patterns:

- `fnmatch <https://docs.python.org/2/library/fnmatch.html>`_ patterns for file names and
- `glob <https://docs.python.org/2/library/glob.html>`_ patterns for directory names.

This is a general rule for the whole library. When you register an action though, you must provide a directory name, **not** a directory name pattern.

We encourage the reader to (re)read the specifications of these two libraries.

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

..  _file_extensions:

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
    
Extensions registered as template file extensions are systematically parsed. What about generated file extensions? They can peacefully coexist with generated files, i.e. existing files 
regardless of their extensions can coexist with generated files and will not be plagued by :program:`cyjenja`. This means that you can safely delete files: only generated files will be deleted [#footnote_existing_files]_.


..  note::
    
    Only generated files are deleted. You can thus safely delete files with :program:`cygenja`.

Actions
----------

Actions (defined in the ``GeneratorAction`` class) are really the core concept of :program:`cygenja`: an action correspond to a *translation rule*. This translation rule makes a correspondance between a subdirectory
and a file pattern and a user callback. Here is the signature of the ``register_action`` method:

..  code-block:: python

    def register_action(self, relative_directory, file_pattern, action_function)
    
The ``relative_directory`` argument holds the name of a relative directory from the *root* directory. Separator is OS dependent. For instance,
under linux, you can register the following:

..  code-block:: python

    engine = Generator(...)
    
    def action_function(...):
        ...
        return ...
        
    engine.register_action('cysparse/sparse/utils', 'find*.cpy', action_function)


This means that all files corresponding to the ``'find*.cpy'`` `fnmatch <https://docs.python.org/2/library/fnmatch.html>`_ pattern inside the ``cysparse/sparse/utils`` 
directory can be dealt with the ``action_function``.

..  only:: html

    Contrary to filters and file extensions, you **cannot** ask for a list of registered actions. But you can ask :program:`cygenja` to perform a `dry` session: :program:`cygenja` outputs what it would normaly do but without
    taking any action [#footnote_treemap_to_string_html]_. 

..  only:: latex

    Contrary to filters and file extensions, you **cannot** ask for a list of registered actions. But you can ask :program:`cygenja` to perform a `dry` session: :program:`cygenja` outputs what it would normaly do but without
    taking any action [#footnote_treemap_to_string_latex]_. 


User callback
"""""""""""""

The ``action_function()`` is a user-defined callback without argument returning a file suffix with a corresponding :program:`Jinja2` 
`variables dict <http://jinja.pocoo.org/docs/dev/templates/#variables>`_ . Let's illustrate this by an example:

..  code-block:: python

    GENERAL_CONTEXT = {...}
    INDEX_TYPES = ['INT32', 'INT64']
    ELEMENT_TYPES = ['FLOAT32', 'FLOAT64']
    
    def generate_following_index_and_type():
        """

        """
        for index in INDEX_TYPES:
            GENERAL_CONTEXT['index'] = index
            for type in ELEMENT_TYPES:
                GENERAL_CONTEXT['type'] = type
                yield '_%s_%s' % (index, type), GENERAL_CONTEXT

The user-defined callback ``generate_following_index_and_type()`` doesn't take any input argument and returns the ``'_%s_%s'`` suffix string together with the variables ``dict`` passed to :program:`Jinja2`.
This function allows :program:`cygenja` to create files with this suffix from any template file. 

For instance, let's use the ``ext_correspondance`` extensions ``dict`` from above (see :ref:`file_extensions`):

..  code-block:: python

    ext_correspondance = { '.cpd' : '.pxd',
                           '.cpx' : 'pyx'}
                               
Any template file with a ``.cpd`` or ``.cpx`` extension will be translated into a ``_index_type.pxd`` or ``_index_type.pyx`` file respectively. The template file ``my_template_code_file.cpd`` will be translated to:

- ``my_template_code_file_INT32_FLOAT32.cpd``
- ``my_template_code_file_INT32_FLOAT64.cpd``
- ``my_template_code_file_INT64_FLOAT32.cpd``
- ``my_template_code_file_INT64_FLOAT64.cpd``

As this function is defined by the user, you have total control on what you want to generate or not. In our example, we redefine ``GENERAL_CONTEXT['index']`` and ``GENERAL_CONTEXT['type']`` for each index and element types.

We use generators (``yield``) but you could return a ``list`` if you prefer.

Incompatible actions
"""""""""""""""""""""

You could register incompatible actions, i.e. register competing actions that would translate a file in different ways. Our approach is to **only** use the first compatible action and to disregard all the other actions, regardless
if they could be applied or not. So the order in which you register your actions is important. A file will be dealt with the **first** compatible action found. This is worth a warning:

..  warning::

    A template is translated with the **first** compatible action found and only that action.
    
Default action
""""""""""""""

:program:`cygenja` allows to define **one** default action that will be triggered when no other compatible action is found for a given 
template file that corresponds to a `fnmatch <https://docs.python.org/2/library/fnmatch.html>`_ pattern:

..  code-block:: python

    engine = Generator(...)
    
    def default_action():
        return ...
    
    engine.register_default_action('*.*',  default_action)

Be careful when defining a default action. This action is be applied to **all** template files (corresponding to the :program:`fnmatch` pattern)for
which no compatible action is found. You might want to prefer declare explicit actions than to rely on this
implicit default action. Use at your own risks. That said, if you have lots of default cases, this
default action can be very convenient and avoid lots of unnecessary action declarations.
        

File generation
-----------------

To generate the files from template files, there is only **one** method to invoke: `generate()`. Its signature is:


..  code-block:: python

    def generate(self, dir_pattern, file_pattern, action_ch='g', recursively=False, force=False)
    

``dir_pattern`` is a ``glob`` pattern taken from the root directory and it is **only** used for directories while ``file_pattern`` is a ``fnmatch`` pattern taken from all matching directories and is **only** used for files.
The ``action_ch`` is a character that trigger different behaviours:

- ``g``: Generate all files that match both directory and file patterns. This is the default behavior.
- ``d``: Same as `g` but with doing anything, i.e. dry run.
- ``c``: Same as `g` but erasing the generated files instead, i.e. clean.
    
These actions can be done in a given directory or in all its corresponding subdirectories. To choose between these two options, use the ``recursively`` switch. Finally, by default, files are only generated if they are 
outdated, i.e. if they are older than the template they were originated from. You can force the generation with the ``force`` switch.
        
..  only:: html

    ..  rubric:: Footnotes
    
..  [#footnote_existing_files] The user is responsible to not to define a translation rule that overwrites any existing files.

..  only:: html

    ..  [#footnote_treemap_to_string_html] You also have access to the internal :class:`TreeMap` object:

        ..  code-block:: python

            engine = Generator(...)
            
            treemap = engine.registered_actions_treemap()

        and thus you have access to all its methods. One interesting method is ``to_string()``. It gives you a representation of all involved subdirectories. 

..  only:: latex

    ..  [#footnote_treemap_to_string_latex] You also have access to the internal :class:`TreeMap` object with the ``registered_actions_treemap()`` method and thus you have access to all its methods. 
        One interesting method is ``to_string()``. It gives you a representation of all involved subdirectories. 

