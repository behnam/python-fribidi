# coding=UTF-8

# TODO: COPYRIGHT

import ctypes


# Memory allocation functions

def int_array(n):

    """
    Return a pointer to allocated C int array of length `n'.
    """

    t = ctypes.c_int * n
    return t()


def int8_array(n):

    """
    Return a pointer to allocated C int array of length `n'.
    """

    t = ctypes.c_int8 * n
    return t()


def int32_array(n):

    """
    Return a pointer to allocated C int32 array of length `n'.
    """

    t = ctypes.c_uint32 * n
    return t()


def int32_array_from_list(a, n=None):

    """
    Return a pointer to allocated C int32 array of length `n', initialized with `a'

    If `n' is not set, the length of `a' will be considered.
    """

    if n is None:
        n = len(a)

    # Memory allocations

    m = int32_array(n)

    for i in xrange(n):
        m[i] = a[i]

    return m


def char_array(n):

    """
    Return a pointer to allocated UTF8 (C char) array of length `n'.
    """

    t = ctypes.c_char * n
    return t()


def char_array_from_string(s):

    """
    Return a pointer to allocated UTF8 (C char) array, initialized with `s'.
    """

    return ctypes.c_char_p(s)

