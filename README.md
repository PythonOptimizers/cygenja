![](doc/source/logo/cygenja-logo64.png)

# cygenja
Cython code generator with Jinja2


Icon made by [Freepik](http://www.freepik.com/) from [flaticon](http://www.flaticon.com/).


## What it is

`cygena` takes templated `Cython` code as input and generates typed `Cython` classes and functions as output. The idea is to mimic the `C++` template mechanism for `Cython` (and disregard the
experimental `Cython` [fused types](http://docs.cython.org/src/userguide/fusedtypes.html)). We use the excellent templating language [Jinja2](http://jinja.pocoo.org/docs/dev/) and some very basic rules.

`cygena` is used in most of our `Cython` projects.

## What it is not

`cygena` is not an automatic `Cython` code generator like the ones listed on [AutoPxd](https://github.com/cython/cython/wiki/AutoPxd). `cygena` does **not** 
parse `C`/`C++` header files to automatically produce Cython bindings.

## Installation

The only dependency is the [Jinja2](http://jinja.pocoo.org/) library.

To install:

```Python
python setup.py install
```

If you want to generate the documentation, you'll need [Sphinx](http://sphinx-doc.org/) and the [sphinx_bootstrap_theme](https://ryan-roemer.github.io/sphinx-bootstrap-theme/README.html) (and possibly [LaTeX](https://www.latex-project.org/) and 
several sub modules/packages).

## Documentation

To know more about the `cygenja` library you can install it and then generate the documentation with `Sphinx`.


## License

`cygenja` is licensed under the GLP3.

