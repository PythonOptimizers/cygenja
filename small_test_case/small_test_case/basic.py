"""
Factory method to access all typed version of `axpy`.
"""
from small_test_case.src.basic_INT32_FLOAT32 import axpy_INT32_FLOAT32
from small_test_case.src.basic_INT32_FLOAT64 import axpy_INT32_FLOAT64
from small_test_case.src.basic_INT64_FLOAT32 import axpy_INT64_FLOAT32
from small_test_case.src.basic_INT64_FLOAT64 import axpy_INT64_FLOAT64
import numpy as np

allowed_types = '\titype:INT32,INT64\n\tdtype:FLOAT32,FLOAT64\n'
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

    if itype == np.int32:
        if dtype == np.float32:
            return axpy_INT32_FLOAT32(m, n, colptr, rowind, values, x, y)
        elif dtype == np.float64:
            return axpy_INT32_FLOAT64(m, n, colptr, rowind, values, x, y)
    elif itype == np.int64:
        if dtype == np.float32:
            return axpy_INT64_FLOAT32(m, n, colptr, rowind, values, x, y)
        elif dtype == np.float64:
            return axpy_INT64_FLOAT64(m, n, colptr, rowind, values, x, y)
    else:
        raise TypeError(type_error_msg)