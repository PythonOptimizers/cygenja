..  _cygenja_use:

=========================================================
Use
=========================================================


The `Generator` class
------------------------

The :class:`Generator` class is the main class of the :program:`cygenja` library. It is also the only 
class the user needs to interact with. It's constructor is really simple:

..  code-block:: python

    from cygenja.generator import Generator
    ...
    
    logger = ...
    engine = Generator('root_directory', logger, True)

The user gives a *root* directory, a *logger* and decides if *warnings* must raise `Exception`\s or not. We describe the root directory a little further in :ref:`root_directory` and develop the two other arguments
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
constructor.



..  _root_directory:

The *root* directory
-----------------------

Filters
--------

File extensions
----------------

Actions
----------

File generation
-----------------



