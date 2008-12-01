#!/usr/bin/env python
# coding=UTF-8

import ctypes
import sys


libfribidi = ctypes.CDLL("libfribidi.so")


def malloc_utf8_array (l):
    Utf8Array = ctypes.c_char * l
    return Utf8Array()

def malloc_utf8_array_from_string (s):
    return ctypes.c_char_p(s)

def malloc_utc32_array (l):
    Utc32Array = ctypes.c_uint32 * l
    return Utc32Array()


def pyunicode_to_utc32_p (a_unicode):
    print
    print 'Enter pyunicode_to_utc32_p'
    print

    utf8_pystr = a_unicode.encode('utf-8')
    utf8_len = len(utf8_pystr)
    utf8_p = malloc_utf8_array_from_string(utf8_pystr)

    print 'utf8_p.value', utf8_p.value
    print 'utf8_len', utf8_len

    utc32_p = malloc_utc32_array(utf8_len+1)
    libfribidi.fribidi_utf8_to_unicode (utf8_p, utf8_len, utc32_p)

    print 'utc32_p [%04x, %04x, %04x, %04x]' % (utc32_p[0], utc32_p[1], utc32_p[2], utc32_p[3])

    print

    # XX: Caller should free it!
    return utc32_p


def utc32_p_to_pyunicode (a_utc32_p, a_len):
    print
    print 'Enter utc32_p_to_pyunicode'
    print

    print 'a_utc32_p [%04x, %04x, %04x, %04x]' % (a_utc32_p[0], a_utc32_p[1], a_utc32_p[2], a_utc32_p[3])

    utf8_p = malloc_utf8_array(6*a_len+1)
    libfribidi.fribidi_unicode_to_utf8 (a_utc32_p, a_len, utf8_p)

    print

    return utf8_p.value



def log2vis (input_pyunicode):
    l = len(input_pyunicode)
    print 'input_pyunicode', input_pyunicode
    print 'l', l
    print

    input_utc32_p = pyunicode_to_utc32_p(input_pyunicode)

    #print libfribidi.fribidi_log2vis()
    output_utc32_p = input_utc32_p

    output_u = utc32_p_to_pyunicode(output_utc32_p, l)
    print 'output_u', output_u



if __name__=='__main__':
    i = u"سلام"

    o = log2vis(i)

    print o

