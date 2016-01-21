"""
Factory method to access all typed version of `axpy`.
"""
{% for index_type in index_list %}
    {% for element_type in type_list %}
from small_test_case.src.basic_@index_type@_@element_type@ import axpy_@index_type@_@element_type@
    {% endfor %}
{% endfor %}
import numpy as np

allowed_types = '\titype:
{%- for index_name in index_list -%}
    @index_name@
    {%- if index_name != index_list|last -%}
    ,
    {%- endif -%}
{%- endfor -%}
\n\tdtype:
{%- for element_name in type_list -%}
    @element_name@
    {%- if element_name != type_list|last -%}
    ,
    {%- endif -%}
{%- endfor -%}
\n'
type_error_msg = 'Arrays have an index and/or element type that is not supported.\n'
type_error_msg += 'Allowed types:\n%s' % allowed_types

def axpy(m, n, colptr, rowind, values, x, y):
    """

    Routine to compute y = Ax + y
    This is done inplace. y will hold the result.

    Matrix A should be supplied in Compressed Sparse Column (CSC) format.

    Creates and returns the right `axpy` based on the element type
    and the index type supplied as input.

    Args:
        m: number of line of matrix A
        n: number of column of matrix A
        colptr: Numpy array pointing to column starts in `rowind` and `values`
        rowind: Numpy array of row indices
        values: Numpy array of values of non zeros elements of A
        x: Numpy array to be multiplied by A
        y: Numpy array to be added to A*x. Also holds the result of
           A*x + y at the end.
    """

    itype = colptr.dtype
    dtype = values.dtype

    assert rowind.dtype == itype
    assert x.dtype == dtype
    assert y.dtype == dtype

{% for index_type in index_list %}
  {% if index_type == index_list |first %}
    if itype == np.@index_type|lower@:
      {% for element_type in type_list %}
        {% if element_type == type_list |first %}
        if dtype == np.@element_type|lower@:
        {% else %}
        elif dtype == np.@element_type|lower@:
        {% endif %}
            return axpy_@index_type@_@element_type@(m, n, colptr, rowind, values, x, y)
      {% endfor %}
  {% else %}
    elif itype == np.@index_type|lower@:
      {% for element_type in type_list %}
        {% if element_type == type_list |first %}
        if dtype == np.@element_type|lower@:
        {% else %}
        elif dtype == np.@element_type|lower@:
        {% endif %}
            return axpy_@index_type@_@element_type@(m, n, colptr, rowind, values, x, y)
      {% endfor %}
  {% endif %}
{% endfor %}
    else:
        raise TypeError(type_error_msg)
