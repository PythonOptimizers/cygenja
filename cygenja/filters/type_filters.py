
def type2enum(type_name):
    """
    Transform a real :program:`CySparse` type into the equivalent :program:`CySparse` enum type.

    For instance:

        INT32_t -> INT32_T

    Args:
        cysparse_type:

    """
    enum_name = type_name[:-1]
    enum_name = enum_name + type_name[-1].upper()

    return enum_name


def cysparse_type_to_numpy_c_type(cysparse_type):
    """
    Transform a :program:`CySparse` enum type into the corresponding :program:`NumPy` C-type.

    For instance:

        INT32_T -> npy_int32

    Args:
        cysparse_type:

    """
    return 'npy_' + str(cysparse_type.lower()[:-2])


def cysparse_type_to_numpy_type(cysparse_type):
    """
    Transform a :program:`CySparse` enum type into the corresponding :program:`NumPy` type.

    For instance:

        INT32_T -> int32

    Args:
        cysparse_type:

    """
    return cysparse_type.lower()[:-2]


def cysparse_type_to_numpy_enum_type(cysparse_type):
    """
    Transform a :program:`Cysparse` enum type into the corresponding :program:`NumPy` enum.

    For instance:

        FLOAT64_T -> NPY_FLOAT64

    Args:
        cysparse_type:
    """
    return 'NPY_' + cysparse_type.upper()[:-2]


def cysparse_type_to_real_sum_cysparse_type(cysparse_type):
    """
    Returns the best **real** type for a **real** sum for a given type.

    For instance:

        INT32_t -> FLOAT64_t

    Args:
        cysparse_type:

    """

    r_type = None

    if cysparse_type in ['INT32_t', 'UINT32_t', 'INT64_t', 'UINT64_t']:
        r_type = 'FLOAT64_t'
    elif cysparse_type in ['FLOAT32_t', 'FLOAT64_t']:
        r_type = 'FLOAT64_t'
    elif cysparse_type in ['FLOAT128_t']:
        r_type = 'FLOAT128_t'
    elif cysparse_type in ['COMPLEX64_t', 'COMPLEX128_t']:
        r_type = 'FLOAT64_t'
    elif cysparse_type in ['COMPLEX256_t']:
        r_type = 'FLOAT128_t'
    else:
        raise TypeError("Not a recognized type")

    assert r_type in ['FLOAT64_t', 'FLOAT128_t']

    return r_type


def cysparse_real_type_from_real_cysparse_complex_type(cysparse_type):
    """
    Returns the **real** type for the real or imaginary part of a **real** complex type.

    For instance:

        COMPLEX128_t -> FLOAT64_t

    Args:
        cysparse:

    """
    r_type = None

    if cysparse_type in ['COMPLEX64_t']:
        r_type = 'FLOAT32_t'
    elif cysparse_type in ['COMPLEX128_t']:
        r_type = 'FLOAT64_t'
    elif cysparse_type in ['COMPLEX256_t']:
        r_type = 'FLOAT128_t'
    else:
        raise TypeError("Not a recognized complex type")

    return r_type
