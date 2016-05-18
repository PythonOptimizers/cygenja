..  _cygenja_examples:

Examples
========

In this section, we demonstrate the use of :program:`cygenja` to generate a small library that performs simple operations

.. math::

    y = Ax + y

where `A` is a matrix supplied in Compressed Sparse Column (CSC) format and x and y are vectors.

Structure of the project
------------------------

.. code-block:: bash

    .
    ├── config
    │   ├── setup.cpy
    │   └── setup.py
    ├── examples
    │   └── demo_axpy.py
    ├── generate_code.py
    ├── generator.log
    ├── setup.py
    ├── site.cfg
    └── small_test_case
    ├── __init__.py
    ├── basic.cpy
    ├── basic.py
    ├── src
    │   ├── __init__.py
    │   ├── basic.cpd
    │   ├── basic.cpx
    │   ├── basic_INT32_FLOAT32.pxd
    │   ├── basic_INT32_FLOAT32.pyx
    │   ├── basic_INT32_FLOAT64.pxd
    │   ├── basic_INT32_FLOAT64.pyx
    │   ├── basic_INT64_FLOAT32.pxd
    │   ├── basic_INT64_FLOAT32.pyx
    │   ├── basic_INT64_FLOAT64.pxd
    │   └── basic_INT64_FLOAT64.pyx
    └── version.py

    4 directories, 22 files


:program:`cygenja` engine
-------------------------

We start by creating a :program:`cygenja` engine in the `generate_code.py` file:

..  code-block:: python

    from cygenja.generator import Generator
    ...

    # read config file
    config = ConfigParser.SafeConfigParser()
    config.read('site.cfg')

    # create logger
    logger = create_logger(config)

    # cygenja engine
    current_directory = os.path.dirname(os.path.abspath(__file__))
    cygenja_engine = Generator(current_directory,
                               GENERAL_ENVIRONMENT,
                               logger=logger)

``create_logger`` is just a wrapper around a `logging <https://docs.python.org/2/library/logging.html>`_ logger. This logger is not mandatory but can be quite handy to debug sessions.
The ``current_directory`` can be absolute or relative. In this example, let's say its value is ``'cysparse'`` [#footnote_absolute_dir_not_really]_, the main project directory.

We now define some global variables representing the different types of data that our code will support:

..  code-block:: python

    INDEX_TYPES = ['INT32', 'INT64']

    REAL_ELEMENT_TYPES = ['FLOAT32', 'FLOAT64']
    ELEMENT_TYPES = ['FLOAT32', 'FLOAT64']

    GENERAL_CONTEXT = {'index_list': INDEX_TYPES,
                       'type_list': ELEMENT_TYPES}



File extensions
---------------

Suppose that our simple test case is written in `Cython <http://cython.org/>`_. We can thus generate four types of files: ``.pyx``, ``.pxd``, ``.pxi`` and of course ``.py`` files. For each type of file, we have defined
a corresponding extension for a template file: ``.cpx``, ``.cpd``, ``.cpi`` and ``cpy``. We register this correspondance like so:

..  code-block:: python

    # register extensions
    cygenja_engine.register_extension('.cpy', '.py')
    cygenja_engine.register_extension('.cpx', '.pyx')
    cygenja_engine.register_extension('.cpd', '.pxd')
    cygenja_engine.register_extension('.cpi', '.pxi')

Now, each time :program:`cygenja` will encounter a template ``.cpx`` file, it will generate one or several corresponding ``.pyx`` files.


Actions
-------

:program:`cygenja` actions are used by the generator to generate files.
Before we can register any :program:`cygenja` actions, we need to define some callbacks. Here are a few examples:

The first action generates only one file without changing its name (the extension will be changed though). To do, we define a callback function

..  code-block:: python

    def single_generation():
        """Only generate one file without any suffix."""
        yield '', GENERAL_CONTEXT

and we have to register this action

..  code-block:: python

    # register actions
    cygenja_engine.register_action('config', '*.*', single_generation)

This registers any template file (``'*.*'``) located in the ``config`` folder with the user callback ``single_generation``.


The second action is more interesting. It generates one file for each index type and for each element type. The generated files will have a new suffix ``_index_type`` attached to their names (eg. ``_INT32_FLOAT64``, ``_INT64_FLOAT64``) and the ``GENERAL_CONTEXT`` ``dict`` is changed every time with the corresponding entry ``index`` updated.

..  code-block:: python

    def generate_following_index_and_element():
        """Generate files following the index and element types."""
        for index in INDEX_TYPES:
            GENERAL_CONTEXT['index'] = index
            for type in ELEMENT_TYPES:
                GENERAL_CONTEXT['type'] = type
                yield '_%s_%s' % (index, type), GENERAL_CONTEXT


Because these functions are user-defined, you have total control and can generate any complicated combinations that you like.

Don't forget to register it

..  code-block:: python

    cygenja_engine.register_action('small_test_case/src', 'basic.*',
                                   generate_following_index_and_element)

This time, we associate template files with the name ``basic`` inside the subdirectory ``small_test_case/src``
with the ``generate_following_index_and_element`` callback.

If you want to associate template files with extension ``.cpi`` to the ``generate_following_index_and_element`` callback inside subdirectory ``generate_following_index_and_element``:

..  code-block:: python

    cygenja_engine.register_action('small_test_case/src',
                                   '*.cpi',
                                   generate_following_index_and_element)

You are allowed to define multiple actions for one subdirectory:

..  code-block:: python

    cygenja_engine.register_action('small_test_case/src',
                                   'find.*',
                                   generate_following_index_and_element)

    cygenja_engine.register_action('small_test_case/src',
                                   'generate_indices.*',
                                   single_generation)

Note that if a template file is associated with several actions, only the **first** action will be triggered.


Filters
-------

`Jinja2 filters <http://jinja.pocoo.org/docs/dev/templates/#filters>`_ are essentially functions that take a string as input and return a modified version of this string. Here is an example in which generic type previously defined are converted to c types:

..  code-block:: python

    def generic_to_c_type(generic_type):
        if generic_type in ['INT32']:
            return 'int'
        elif generic_type in ['INT64']:
            return 'long'
        elif generic_type in ['FLOAT32']:
            return 'float'
        elif generic_type in ['FLOAT64']:
            return 'double'
        else:
            raise TypeError("Not a recognized generic type")

Once the filter is created, it needs to be registered within the generator.
We keep the same name for the function as the function name itself to register it (this is not mandatory):

..  code-block:: python

    cygenja_engine.register_filter('generic_to_c_type',
                                   generic_to_c_type)




Writing templates
-----------------
Now you can use ``generic_to_c_type`` in your :program:`Jinja2` templates.

TODO: describe how to use jinja filters

.. literalinclude:: ../../small_test_case/small_test_case/src/basic.cpx
   :linenos:


File generation
---------------

We are now ready to generate some files from some templates. There is only one method to call: ``generate``. Its signature is:

..  code-block:: python

    engine.generate(dir_pattern, file_pattern, action_ch='g', recursively=True, force=False)

where ``dir_pattern`` is a :program:`glob` pattern used to match directories and ``file_pattern`` a :program:`fnmatch` pattern taken from all matching directories. This combination allows you to refine your operations with
a great flexibility. The ``action_ch`` argument can be ``g`` (generate files), ``c`` (clean or erase files) or ``d`` (dry run).

This is the beginning of the output :program:`cygenja` generates when asked a dry run for **all** file generation:

..  code-block:: bash

    2016-05-17 22:39:39,277 - INFO - Start some action(s)
    Process file 'config/setup.cpy' with function 'single_generation':
       -> config/setup.py
    Process file 'small_test_case/basic.cpy' with function 'single_generation':
       -> small_test_case/basic.py
    Process file 'small_test_case/src/basic.cpd' with function 'generate_following_index_and_element':
       -> small_test_case/src/basic_INT32_FLOAT32.pxd
       -> small_test_case/src/basic_INT32_FLOAT64.pxd
       -> small_test_case/src/basic_INT64_FLOAT32.pxd
       -> small_test_case/src/basic_INT64_FLOAT64.pxd
    Process file 'small_test_case/src/basic.cpx' with function 'generate_following_index_and_element':
       -> small_test_case/src/basic_INT32_FLOAT32.pyx
       -> small_test_case/src/basic_INT32_FLOAT64.pyx
       -> small_test_case/src/basic_INT64_FLOAT32.pyx
       -> small_test_case/src/basic_INT64_FLOAT64.pyx
    ...

A total of 10 files will be generated.

Source code of this example
---------------------------

All the source for this example are available on GitHub at `https://github.com/PythonOptimizers/cygenja/tree/develop/small_test_case <https://github.com/PythonOptimizers/cygenja/tree/develop/small_test_case>`_.


..  only:: html

    ..  rubric:: Footnotes

..  [#footnote_absolute_dir_not_really] Yes, we are well aware that this not what is expected from the code. ``os.path.abspath(__file__)`` will never only return ``small_test_case``.
