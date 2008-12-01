#!/usr/bin/env python
# coding=UTF-8

import ctypes
import sys


libfribidi = ctypes.CDLL("libfribidi.so")


def _malloc_utf8_array (l):
    """
    Returns a pointer to allocated UTF8 (C char) array of length `l'
    """

    Utf8Array = ctypes.c_char * l
    return Utf8Array()

def _malloc_utf8_array_from_string (s):
    """
    Returns a pointer to allocated UTF8 (C char) array, initialized with value of `s'
    """

    return ctypes.c_char_p(s)

def _malloc_utc32_array (l):
    """
    Returns a pointer to allocated UTC32 (C int32) array of length `l'
    """

    Utc32Array = ctypes.c_uint32 * l
    return Utc32Array()


def _pyunicode_to_utc32_p (a_pyunicode):
    """
    Converts Python Unicode instance to UTC32 (C int32) array

    Note: Caller should free the allocated memory of returned pointer
    """

    a_len = len(a_pyunicode)

    print 'a_len', a_len

    utf8_pystr = a_pyunicode.encode('utf-8')
    utf8_len = len(utf8_pystr)
    utf8_p = _malloc_utf8_array_from_string(utf8_pystr)

    print 'utf8_p.value', utf8_p.value
    print 'utf8_len', utf8_len

    utc32_p = _malloc_utc32_array(a_len+1)
    libfribidi.fribidi_utf8_to_unicode (utf8_p, utf8_len, utc32_p)

    print 'utc32_p [%04x, %04x, %04x, %04x]' % (utc32_p[0], utc32_p[1], utc32_p[2], utc32_p[3])

    print

    # XX: Caller should free it!
    return utc32_p


def _utc32_p_to_pyunicode (a_utc32_p):
    """
    Converts UTC32 (C int32) array to Python Unicode instance
    """

    print 'a_utc32_p [%04x, %04x, %04x, %04x]' % (a_utc32_p[0], a_utc32_p[1], a_utc32_p[2], a_utc32_p[3])

    utc32_len = ctypes.sizeof(a_utc32_p) / ctypes.sizeof(ctypes.c_uint32) - 1
    print 'utc32_len', utc32_len

    utf8_len = 6*utc32_len+1
    utf8_p = _malloc_utf8_array(utf8_len)

    libfribidi.fribidi_unicode_to_utf8 (a_utc32_p, utc32_len, utf8_p)

    print

    return utf8_p.value



def log2vis (input_pyunicode):
    print 'input_pyunicode', input_pyunicode

    input_utc32_p = _pyunicode_to_utc32_p(input_pyunicode)

    #print libfribidi.fribidi_log2vis()
    output_utc32_p = input_utc32_p

    output_u = _utc32_p_to_pyunicode(output_utc32_p)
    print 'output_u', output_u



if __name__=='__main__':
    i = u"سلام"

    o = log2vis(i)

    print o

