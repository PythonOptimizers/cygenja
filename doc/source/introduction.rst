..  _cygenja_introduction:

=========================================================
Introduction
=========================================================

:program:`cygenja` is a little utility to generate typed source files from
`Jinja2 <http://jinja.pocoo.org/docs/dev/>`_ source templates. We use it extensively to generate our `Cython <http://cython.org/>`_
projects. We provide this tool as is. See :ref:`limitations` to see if this tool 
is for you.


What it can do
==================

From a bunch of templated (source) files, it can generate several (source) files. The translation part is given to the powerful `Jinja2 <http://jinja.pocoo.org/docs/dev/>`_ template engine. 
:program:`cygenja` is a layer above this template engine and is in charge to dispatch translation rules in the right subdirectories and apply them to the right bunch of files. A file is only generated if it is older than 
the template file used to produced it, i.e. a change in a template file triggers a regeneration of the corresponding files [#force_generation]_.  
 
How it works
==================

Within a *root* directory, you provide some translation rules: each rule is attached to a subdirectory and a file pattern. You can even define several rules for one subdirectory.
These rules (called `actions` in :program:`cygenja`) are user defined *callbacks*. Once all rules are registered, the :program:`cygenja` engine 
is given a directory pattern and a file pattern: only the matching rules are triggered. See :ref:`cygenja_use` or look at the :ref:`cygenja_examples` for more.

..  _limitations:

Limitations
==================

Here is a small list of limitations [#footnote_limitations]_. It is of course not exhaustive but it can already give you a hint if this tool is right for you or not.

:program:`cygenja` only parses subdirectories
-----------------------------------------------

:program:`cygenja` can only parse subdirectories from a root directory. This means
that it **cannot** generate files located at the root directory level (or outside the root directory).

:program:`cygenja` generates files in place
--------------------------------------------

Files can only be generated in the same subdirectories as their corresponding templates.

Templates and generated files **must** have different extensions
-----------------------------------------------------------------

Templates are recognized if they have specific extensions. The corresponding generated files will be given specific corresponding extensions too. In fact, this extension correspondance is defined by the user but both extensions 
**must** be different. For instance, `*.cpd` templated files are transformed into `*.pxd` files. Both extensions, `.cpd` and `.pxd` **must** be different.

File patterns: only :program:`fnmatch` patterns
-------------------------------------------------

Translation rules can only be applied to files corresponding to `fnmatch <https://docs.python.org/2/library/fnmatch.html>`_ patterns. While this covers most cases, it might be a limitation for some.

We also use the same kind of file patterns to trigger the translation.

Directory patterns: only :program:`glob` patterns
-------------------------------------------------

To select the subdirectory(ies) within which the rules will be applied by :program:`cygenja`'s engine, only  `glob <https://docs.python.org/2/library/glob.html>`_ patterns can be used.

Contradictory *actions* are not filtered or monitored
-----------------------------------------------------

Nothing prevents you to register conflicting actions. In this case, only the last registered action is certain to be triggered.

..  only:: html

    .. rubric:: Footnotes
    
..  [#force_generation] Of course, you can force a file generation.

.. [#footnote_limitations] Although most limitations described here can easily be overcome.
