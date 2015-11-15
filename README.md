# cygenja
Cython code generator with Jinja2

## What it is

`cygena` takes templated `Cython` code as input and generates typed `Cython` classes and functions as output. The idea is to mimic the `C++` template mechanism for `Cython` (and disregard the
experimental `Cython` [fused types](http://docs.cython.org/src/userguide/fusedtypes.html)). We use the excellent templating language [Jinja2](http://jinja.pocoo.org/docs/dev/) and some very basic rules.

`cygena` is used in most of our `Cython` projects.

## What it is not

`cygena` is not an automatic `Cython` code generator like the ones listed on [AutoPxd](https://github.com/cython/cython/wiki/AutoPxd). `cygena` does **not** 
parse `C`/`C++` header files to automatically produce Cython bindings.




