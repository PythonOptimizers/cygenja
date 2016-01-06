cygenja
=======================

`cygenja` is a very simple code generator.

What it is
-----------

`cygena` takes templated `Cython` code as input and generates typed `Cython` classes and functions. The idea is to mimic the `C++` template mechanism for `Cython` (and disregard the
experimental `Cython` `fused types <http://docs.cython.org/src/userguide/fusedtypes.html>`_. We use the excellent templating language `Jinja2 <http://jinja.pocoo.org/docs/dev/>`_) and some very basic rules.

`cygena` is used in most of our `Cython` projects.

What it is not
-----------------

`cygena` is not an automatic `Cython` code generator like the ones listed on `AutoPxd <https://github.com/cython/cython/wiki/AutoPxd>`_. `cygena` does **not**
parse `C`/`C++` header files to automatically produce Cython bindings.



