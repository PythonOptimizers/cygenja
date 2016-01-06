..  _cygenja_examples:

=========================================================
Examples
=========================================================

In this section, we demonstrate the use of :program:`cygenja` to generate the `CySparse <https://github.com/PythonOptimizers/cysparse>`_ library.

Init
-----

We start by creating a :program:`cygenja` engine:


..  code-block:: python

    from cygenja.generator import Generator
    ...
    
    # read cysparse.cfg
    cysparse_config = ConfigParser.SafeConfigParser()
    cysparse_config.read('cysparse.cfg')

    # create logger
    logger = make_logger(cysparse_config=cysparse_config)

    # cygenja engine
    current_directory = os.path.dirname(os.path.abspath(__file__))
    cygenja_engine = Generator(current_directory, logger=logger)

``make_logger`` is just a wrapper around a `logging <https://docs.python.org/2/library/logging.html>`_ logger. This logger is not mandatory but can be quite handy to debug sessions. 
The ``current_directory`` can be absolute or relative. In this example, let's say its value is ``'cysparse'`` [#footnote_absolute_dir_not_really]_, the main project directory.

We now define some variables:

..  code-block:: python

    ELEMENT_TYPES = ['INT32_t', 'INT64_t', 
                     'FLOAT32_t', 'FLOAT64_t', 'FLOAT128_t', 
                     'COMPLEX64_t', 'COMPLEX128_t', 'COMPLEX256_t']
    INDEX_TYPES = ['INT32_t', 'INT64_t']
    ...
        
    GENERAL_CONTEXT = {
                    'type_list': ELEMENT_TYPES,
                    'index_list' : INDEX_TYPES,
                    'default_index_type' : DEFAULT_INDEX_TYPE,
                    'integer_list' : INTEGER_ELEMENT_TYPES,
                    'real_list' : REAL_ELEMENT_TYPES,
                    'complex_list' : COMPLEX_ELEMENT_TYPES,
                    ...                   
                  }



File extensions
-----------------

:program:`CySparse` is written essentially in `Cython <http://cython.org/>`_. We can thus generate four types of files: ``.pyx``, ``.pxd``, ``.pxi`` and of course ``.py`` files. For each type of file, we have defined
a corresponding extension for a template file: ``.cpx``, ``.cpd``, ``.cpi`` and ``cpy``. We register this correspondance like so:

..  code-block:: python

    # register extensions
    cygenja_engine.register_extension('.cpy', '.py')
    cygenja_engine.register_extension('.cpx', '.pyx')
    cygenja_engine.register_extension('.cpd', '.pxd')
    cygenja_engine.register_extension('.cpi', '.pxi')

Now, each time :program:`cygenja` will encounter a template ``.cpx`` file, it will generate one or several corresponding ``.pyx`` files.

Filters
---------

`Jinja2 filters <http://jinja.pocoo.org/docs/dev/templates/#filters>`_ are essentially functions that take a string as input and return a modified version of this string. Here is an example:

..  code-block:: python

    def cysparse_type_to_numpy_c_type(cysparse_type):
        """
        Transform a :program:`CySparse` enum type into the corresponding 
        :program:`NumPy` C-type.

        For instance:

            INT32_T -> npy_int32

        Args:
            cysparse_type:

        """
        return 'npy_' + str(cysparse_type.lower()[:-2])
        
We keep the same name for the function as the function name itself to register it (this is not mandatory):

..  code-block:: python

    engine.register_filter('cysparse_type_to_numpy_c_type', cysparse_type_to_numpy_c_type)
    
Now you can use ``cysparse_type_to_numpy_c_type()`` in your :program:`Jinja2` template [#footnote_our_jinja2_env]_:

..  code-block:: jinja

    cnp.ndarray[cnp.@index|cysparse_type_to_numpy_c_type@, ndim=1] a_row = 
        cnp.PyArray_SimpleNew( 1, dmat, cnp.@index|cysparse_type_to_numpy_enum_type@)   
        
Actions
---------

Before we can register any :program:`cygenja` actions, we need to define some callbacks. Here are a few examples:

..  code-block:: python

    def single_generation():
        yield '', GENERAL_CONTEXT


    def generate_following_only_index():
        GENERAL_CONTEXT['type'] = None
        for index in INDEX_TYPES:
            GENERAL_CONTEXT['index'] = index

            yield '_%s' % index, GENERAL_CONTEXT

The first function, ``single_generation``, only generates one file without changing its name (the extension will be changed though). The second function, ``generate_following_only_index``, is more interesting. It generates one file for each index type. These files 
all have a suffix ``_index`` attached to their names (i.e. ``_INT32_t``, ``_INT64_t``) and the ``GENERAL_CONTEXT`` ``dict`` is changed every time with the corresponding entry ``index`` updated. Here is a more complex version where we generate files with 
respect to an index type but also an element type:

..  code-block:: python

    def generate_following_index_and_element():
        for index in INDEX_TYPES:
            GENERAL_CONTEXT['index'] = index
            for type in ELEMENT_TYPES:
                GENERAL_CONTEXT['type'] = type
                yield '_%s_%s' % (index, type), GENERAL_CONTEXT

Because these functions are user-defined, you have total control and can generate any complicated combinations that you like.

Now we can use these callbacks and register them. For instance:

..  code-block:: python

    engine.register_action('config', '*.*', single_generation)
    
This registers any template file (``'*.*'``) located in ``cysparse/config`` (linux version) with the user callback ``single_generation``.

..  code-block:: python

    engine.register_action('cysparse/sparse/sparse_utils/generic', 
                           'generate_indices.*', 
                           generate_following_only_index)

This time, we associate template files with the name ``generate_indices`` inside the subdirectory ``cysparse/sparse/sparse_utils/generic``  
with the ``generate_following_only_index`` callback [#remember_the_root_directory]_.

Here, we only associate template files with extension ``.cpi`` to the ``generate_following_index_and_element`` callback inside subdirectory ``cysparse/sparse/csc_mat_matrices/csc_mat_kernel``:

..  code-block:: python

    cygenja_engine.register_action('cysparse/sparse/csc_mat_matrices/csc_mat_kernel', 
                                   '*.cpi', 
                                   generate_following_index_and_element)  

You are allowed to define multiple actions for one subdirectory:

..  code-block:: python

    cygenja_engine.register_action('cysparse/sparse/sparse_utils/generic', 
                                   'find.*', 
                                   generate_following_index_and_element)
                                   
    cygenja_engine.register_action('cysparse/sparse/sparse_utils/generic', 
                                   'generate_indices.*', 
                                   generate_following_only_index)

Remember that if a template file can be associated with several actions, only the **first** action will be triggered.

File generation
------------------

We are now ready to generate some files from some templates. There is only one method to call: ``generate``. Its signature is:

..  code-block:: python

    engine.generate(dir_pattern, file_pattern, action_ch='g', recursively=True, force=False)

where ``dir_pattern`` is a :program:`glob` pattern used to match directories and ``file_pattern`` a :program:`fnmatch` pattern taken from all matching directories. This combination allows you to refine your operations with 
a great flexibility. The ``action_ch`` argument can be ``g`` (generate files), ``c`` (clean or erase files) or ``d`` (dry run).

This is the beginning of the output :program:`cygenja` generates when asked a dry run for **all** file generation:

..  code-block:: bash

    Process file 'config/setup.cpy' with function 'single_generation':
       -> config/setup.py
    Process file 'cysparse/sparse/ll_mat.cpx' with function 'single_generation':
       -> cysparse/sparse/ll_mat.pyx
    Process file 'cysparse/sparse/csc_mat_matrices/csc_mat.cpx' with 
                                function 'generate_following_index_and_element':
       -> cysparse/sparse/csc_mat_matrices/csc_mat_INT32_t_INT32_t.pyx
       -> cysparse/sparse/csc_mat_matrices/csc_mat_INT32_t_INT64_t.pyx
       -> cysparse/sparse/csc_mat_matrices/csc_mat_INT32_t_FLOAT32_t.pyx
       -> cysparse/sparse/csc_mat_matrices/csc_mat_INT32_t_FLOAT64_t.pyx
       -> cysparse/sparse/csc_mat_matrices/csc_mat_INT32_t_FLOAT128_t.pyx
       -> cysparse/sparse/csc_mat_matrices/csc_mat_INT32_t_COMPLEX64_t.pyx
       -> cysparse/sparse/csc_mat_matrices/csc_mat_INT32_t_COMPLEX128_t.pyx
    ...
    
At the moment of writing, we have 23 registered actions that trigger 492 file generations.
                                     
..  only:: html

    ..  rubric:: Footnotes

..  [#footnote_absolute_dir_not_really] Yes, we are well aware that this not what is expected from the code. ``os.path.abspath(__file__)`` will never only return ``cysparse``.
    
..  [#footnote_our_jinja2_env] :program:`CySparse`'s :program:`Jinja2` environment allows us to use variables names like so: ``@my_variable@``.

..  [#remember_the_root_directory] Thus the real directory is ``cysparse/cysparse/sparse/sparse_utils/generic``.
