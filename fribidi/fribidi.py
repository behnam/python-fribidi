#!/usr/bin/env python
# coding=UTF-8

# TODO: COPYRIGHT

"""
implementation of Unicode Bidirectional Algorithm, using GNU FriBidi

This is a python wrap of GNU FriBidi C library.
http://fribidi.org/

GNU FriBidi is an implementation of Unicode Bidirectional Algorithm (bidi).
http://unicode.org/reports/tr9/
"""

__version__ = '0.11'


# Package imports

try:
    import _malloc
    from _type import Mask, _Type, CharType, ParType
except ImportError:
    from . import _malloc
    from ._type import Mask, _Type, CharType, ParType


# Python version

import types

try:
    # Python 2.x
    UnicodeType = types.UnicodeType
except AttributeError:
    # Python 3.0
    StringTypes = str


# Load FriBidi

import ctypes

class VersionError(Exception):
    pass

_libfribidi = ctypes.CDLL("libfribidi.so")
_libfribidi._orig_getitem = _libfribidi.__getitem__
def _libfribidi_new_getitem(name):
    try:
        return _libfribidi._orig_getitem(name)
    except AttributeError:
        raise VersionError
_libfribidi.__getitem__ = _libfribidi_new_getitem


# TODO: better version detection
try:
    _libfribidi.fribidi_shape()
except VersionError:
    libfribidi_version = '0.10'
else:
    libfribidi_version = '0.19'
libfribidi_version_info = [int(x) for x in libfribidi_version.split('.')]


# Unicode type convertors

def _pyunicode_to_utf32_p(a_pyunicode):
    """Return UTF32 (C int32) array from Py_Unicode.
    """

    a_len = len(a_pyunicode)

    utf8_pystr = a_pyunicode.encode('UTF-8')
    utf8_len = len(utf8_pystr)
    utf8_p = _malloc.char_array_from_string(utf8_pystr)

    utf32_p = _malloc.int32_array(a_len+1)
    _libfribidi.fribidi_utf8_to_unicode(utf8_p, utf8_len, utf32_p)

    return utf32_p


def _utf32_p_to_pyunicode(a_utf32_p):
    """Return Py_Unicode from UTF32 (C int32) array.
    """

    utf32_len = ctypes.sizeof(a_utf32_p) / ctypes.sizeof(ctypes.c_uint32)

    utf8_len = 6*utf32_len+1
    utf8_p = _malloc.char_array(utf8_len)

    _libfribidi.fribidi_unicode_to_utf8(a_utf32_p, utf32_len, utf8_p)

    return utf8_p.value.decode('UTF-8')


# TODO: More dir functions (probabely should put into Type class)
# fribidi-bidi-types.h: 283-334


# Functions

def get_bidi_types(unicode_text, text_length=None):
    """
    Return characters bidi types.

    This function returns the bidi type of a character as defined in Table 3.7
    Bidirectional Character Types of the Unicode Bidirectional Algorithm
    available at
    http://www.unicode.org/reports/tr9/#Bidirectional_Character_Types, using
    data provided in file UnicodeData.txt of the Unicode Character Database
    available at http://www.unicode.org/Public/UNIDATA/UnicodeData.txt .
    """
    # TODO: There are a few macros defined in fribidi-bidi-types.h for querying a bidi type.


    if not isinstance(unicode_text, unicode):
        unicode_text = unicode(unicode_text)

    if not text_length:
        text_length = len(unicode_text)

    # Memory allocations

    input_utf32_p = _pyunicode_to_utf32_p(unicode_text)

    output_chartype_p = _malloc.int32_array(text_length)

    # Calling the API
    """
    FRIBIDI_ENTRY void fribidi_get_bidi_types (
        const FriBidiChar *str,     /* input string */
        const FriBidiStrIndex len,  /* input string length */
        FriBidiCharType *btypes     /* output bidi types */
    );
    """

    if libfribidi_version <= 10:
        _libfribidi.fribidi_get_types(
            input_utf32_p,          # input string
            text_length,            # input string length
            output_chartype_p       # output bidi types
        )

    else:
        _libfribidi.fribidi_get_bidi_types(
            input_utf32_p,          # input string
            text_length,            # input string length
            output_chartype_p       # output bidi types
        )

    # Pythonizing the output

    return [i for i in output_chartype_p]


# TODO: fribidi_get_bidi_type_name


# ########################################################################
# FriBidi API, Bidi (fribidi-bidi.h)


def get_par_direction(bidi_types_list, text_length=None):
    """
    Return base paragraph direction

    No weak paragraph direction is returned, only LTR, RTL, or ON.

    Input: List of bidi types as returned by get_bidi_types()

    This function finds the base direction of a single paragraph,
    as defined by rule P2 of the Unicode Bidirectional Algorithm available at
    http://www.unicode.org/reports/tr9/#P2.

    You typically do not need this function as get_par_embedding_levels() knows
    how to compute base direction itself, but you may need this to implement a
    more sophisticated paragraph direction handling.

    Note that you can pass more than a paragraph to this function and the
    direction of the first non-neutral paragraph is returned, which is a very
    good heuristic to set direction of the neutral paragraphs at the beginning
    of text.  For other neutral paragraphs, you better use the direction of the
    previous paragraph.
    """

    if not text_length:
        text_length = len(bidi_types_list)

    # Memory allocations

    input_bidi_types_p = _malloc.int32_array_from_list(bidi_types_list, text_length)

    # Calling the API

    '''
    FRIBIDI_ENTRY FriBidiParType fribidi_get_par_direction (
      const FriBidiCharType *bidi_types,    /* input list of bidi types as returned by fribidi_get_bidi_types() */
      const FriBidiStrIndex len             /* input string length */
    );
    '''

    par_type = _libfribidi.fribidi_get_par_direction(
        input_bidi_types_p, # input bidi types
        text_length         # input string length
    )

    # Pythonizing the output

    return int(par_type)


def get_par_embedding_levels(bidi_types_list, text_length=None,
                                base_direction=None):
    """
    Return the list of embedding levels of characters in the paragraph.

    A tuple of list of embedding levels, resolved paragraph direction, and
    maximum embedding level will be returned.

    Input: List of bidi types as returned by get_bidi_types()

    This function finds the bidi embedding levels of a single paragraph,
    as defined by the Unicode Bidirectional Algorithm available at
    http://www.unicode.org/reports/tr9/.  This function implements rules P2 to
    I1 inclusive, and parts 1 to 3 of L1, except for rule X9 which is
    implemented in remove_bidi_marks().  Part 4 of L1 is implemented in
    reorder_line().
    """

    # TODO: There are a few macros defined in fribidi-bidi-types.h to work with this embedding levels.

    if not text_length:
        text_length = len(bidi_types_list)

    if base_direction is None:
        base_direction=ParType.LTR

    # Memory allocations

    input_bidi_types_p = _malloc.int32_array_from_list(bidi_types_list, text_length)
    pbase_dir_p = ctypes.pointer(ctypes.c_int32(base_direction))

    emb_p = _malloc.int8_array(text_length)

    # Calling the API
    """
    FRIBIDI_ENTRY FriBidiLevel fribidi_get_par_embedding_levels (
        const FriBidiCharType *bidi_types,  /* input list of bidi types as returned by fribidi_get_bidi_types() */
        const FriBidiStrIndex len,          /* input string length of the paragraph */
        FriBidiParType *pbase_dir,          /* requested and resolved paragraph base direction */
        FriBidiLevel *embedding_levels      /* output list of embedding levels */
    ) FRIBIDI_GNUC_WARN_UNUSED;
    """

    success = _libfribidi.fribidi_get_par_embedding_levels(
        input_bidi_types_p, # input list of bidi types as returned by get_bidi_types()
        text_length,        # input string length of the paragraph
        pbase_dir_p,        # requested and resolved paragraph base direction
        emb_p               # output list of embedding levels
    )

    if not success:
        raise Exception('fribidi_get_par_embedding_levels failed')

    # Pythonizing the output

    max_levels = success - 1

    output_levels_list = [i for i in emb_p]

    return [output_levels_list, pbase_dir_p[0], max_levels]


def reorder_line(bidi_types_list, text_length=None, line_offset=0,
                    base_direction=None, with_max_levels=False):
    """
    Return visual reordered of a line of logical string
    """

    # TODO
    """
    This function reorders the characters in a line of text from logical to
    final visual order.  This function implements part 4 of rule L1, and rules
    L2 and L3 of the Unicode Bidirectional Algorithm available at
    http://www.unicode.org/reports/tr9/#Reordering_Resolved_Levels.

    As a side effect it also sets position maps if not NULL.

    You should provide the resolved paragraph direction and embedding levels as
    set by fribidi_get_par_embedding_levels().  Also note that the embedding
    levels may change a bit.  To be exact, the embedding level of any sequence
    of white space at the end of line is reset to the paragraph embedding level
    (That is part 4 of rule L1).

    Note that the bidi types and embedding levels are not reordered.  You can
    reorder these (or any other) arrays using the map later.  The user is
    responsible to initialize map to something sensible, like an identity
    mapping, or pass NULL if no map is needed.

    There is an optional part to this function, which is whether non-spacing
    marks for right-to-left parts of the text should be reordered to come after
    their base characters in the visual string or not.  Most rendering engines
    expect this behavior, but console-based systems for example do not like it.
    This is controlled by the FRIBIDI_FLAG_REORDER_NSM flag.  The flag is on
    in FRIBIDI_FLAGS_DEFAULT.

    Returns: Maximum level found in this line plus one, or zero if any error
    occured (memory allocation failure most probably).
    """

    if not text_length:
        text_length = len(bidi_types_list)

    if base_direction is None:
        base_direction=ParType.LTR

    # Memory allocations

    input_bidi_types_p = _malloc.int32_array_from_list(bidi_types_list, text_length)
    pbase_dir_p = ctypes.pointer(ctypes.c_int32(base_direction))

    emb_p = _malloc.int8_array(text_length)

    # Calling the API
    """
    FRIBIDI_ENTRY FriBidiLevel fribidi_reorder_line (
        FriBidiFlags flags,                 /* reorder flags */
        const FriBidiCharType *bidi_types,  /* input list of bidi types as returned by fribidi_get_bidi_types() */
        const FriBidiStrIndex len,          /* input length of the line */
        const FriBidiStrIndex off,          /* input offset of the beginning of the line in the paragraph */
        const FriBidiParType base_dir,      /* resolved paragraph base direction */
        FriBidiLevel *embedding_levels,     /* input list of embedding levels, as returned by fribidi_get_par_embedding_levels */
        FriBidiChar *visual_str,            /* visual string to reorder */
        FriBidiStrIndex *map                /* a map of string indices which is reordered to reflect where each glyph ends up. */
    ) FRIBIDI_GNUC_WARN_UNUSED;
    """

    success = _libfribidi.fribidi_get_par_embedding_levels(
        input_flags,        # reorder flags
        input_bidi_types_p, # input list of bidi types as returned by get_bidi_types()
        text_length,        # input string length of the paragraph
        line_offset,        # input offset of the beginning of the line in the paragraph
        pbase_dir_p,        # requested and resolved paragraph base direction
        emb_p,               # output list of embedding levels
        embedding_levels_p  # input list of embedding levels, as returned by get_par_embedding_levels()
    )

    if not success:
        raise Exception('fribidi_get_par_embedding_levels failed')

    # Pythonizing the output

    max_levels = success - 1

    output_levels_list = [i for i in emb_p]

    if with_max_levels:
        return [output_levels_list, max_levels]
    else:
        return output_levels_list



# ########################################################################
# FriBidi API, Misc

def log2vis(unicode_text, text_length=None, base_direction=None,
            with_l2v_position=False, with_v2l_position=False,
            with_embedding_level=False):
    """
    Return a unicode text contaning the visual order of characters in the text.

    If paragraph direction is not set (`base_direction'), it will be assumed to
    to be letf-to-right (LTR).

    If any of with_l2v_position, with_v2l_position, and with_embedding_level
    are True, the return value will be a tuple including logical-to-visual
    position, visual-to-logical positions, or embedding-level lists
    respectively.
    """

    if not isinstance(unicode_text, unicode):
        unicode_text = unicode(unicode_text)

    if not text_length:
        text_length = len(unicode_text)

    if base_direction is None:
        base_direction=ParType.LTR


    # Memory allocations

    input_utf32_p = _pyunicode_to_utf32_p(unicode_text)
    pbase_dir_p = ctypes.pointer(ctypes.c_int32(base_direction))

    output_utf32_p = _malloc.int32_array(text_length+1)

    l2v_p = _malloc.int_array(text_length)  if with_l2v_position    else None
    v2l_p = _malloc.int_array(text_length)  if with_v2l_position    else None
    emb_p = _malloc.int8_array(text_length) if with_embedding_level else None

    # Calling the API
    """
    FRIBIDI_API fribidi_boolean fribidi_log2vis (

        /* input */
        FriBidiChar     *str,
        FriBidiStrIndex len,
        FriBidiCharType *pbase_dirs,

        /* output */
        FriBidiChar     *visual_str,
        FriBidiStrIndex *position_L_to_V_list,
        FriBidiStrIndex *position_V_to_L_list,
        FriBidiLevel    *embedding_level_list
    );
    """

    successed = _libfribidi.fribidi_log2vis(
        # input
        input_utf32_p,
        text_length,
        pbase_dir_p,

        # output
        output_utf32_p,
        l2v_p,
        v2l_p,
        emb_p
    )

    if not successed:
        raise Exception('fribidi_log2vis failed')

    # Pythonizing the output

    output_u = _utf32_p_to_pyunicode(output_utf32_p)

    if with_l2v_position or with_v2l_position or with_embedding_level:
        res = (output_u, )
        if with_l2v_position:       res += ([i for i in l2v_p], )
        if with_v2l_position:       res += ([i for i in v2l_p], )
        if with_embedding_level:    res += ([i for i in emb_p], )

    else:
        res = output_u

    return res


def log2vis_get_embedding_levels(unicode_text, base_direction=None):
    """
    Return an array containing the embedding-level of characters in the text.
    """

    if not isinstance(unicode_text, unicode):
        unicode_text = unicode(unicode_text)

    if base_direction is None:
        base_direction=ParType.LTR

    text_len = len(unicode_text)

    # Memory allocations

    input_utf32_p = _pyunicode_to_utf32_p(unicode_text)
    pbase_dir_p = ctypes.pointer(ctypes.c_int32(base_direction))

    emb_p = _malloc.int8_array(text_len)

    # Calling the API
    """
    FRIBIDI_API fribidi_boolean fribidi_log2vis_get_embedding_levels (

        /* input */
        FriBidiChar     *str,
        FriBidiStrIndex len,
        FriBidiCharType *pbase_dir,

        /* output */
        FriBidiLevel    *embedding_level_list
    );
    """

    successed = _libfribidi.fribidi_log2vis_get_embedding_levels(
        # input
        input_utf32_p,
        text_len,
        pbase_dir_p,

        # output
        emb_p
    )

    if not successed:
        raise Exception('fribidi_log2vis_get_embedding_levels failed')

    # Pythonizing the output

    res = [i for i in emb_p]

    return res


def remove_bidi_marks(unicode_text, text_length=None,
                        with_position_to=False, with_position_from=False,
                        with_embedding_level=False):
    """
    Return the text with all Bidirectional Marks removed.

    If with_position_to, with_position_from, or with_embedding_level are True,
    the return value will be a tuple including positions from input text to
    output text, positions from output text to input text, or embedding-level
    lists respectively.

    Note: Seems the optional parameters of fribidi_remove_bidi_marks() doesn't
    work or crash.  Use them at your own risk.
    """

    if not isinstance(unicode_text, unicode):
        unicode_text = unicode(unicode_text)

    if not text_length:
        text_length = len(unicode_text)

    # Memory allocations

    input_utf32_p = _pyunicode_to_utf32_p(unicode_text)

    pto_p = _malloc.int_array(text_length)  if with_position_to     else None
    pfr_p = _malloc.int_array(text_length)  if with_position_from   else None
    emb_p = _malloc.int8_array(text_length) if with_embedding_level else None

    # Calling the API
    """
    FRIBIDI_API FriBidiStrIndex fribidi_remove_bidi_marks (

        /* input & output */
        FriBidiChar     *str,

        /* input */
        FriBidiStrIndex length,

        /* output */
        FriBidiStrIndex *position_to_this_list,
        FriBidiStrIndex *position_from_this_list,
        FriBidiLevel    *embedding_level_list
    );
    """

    new_length = _libfribidi.fribidi_remove_bidi_marks(
        # input & output
        input_utf32_p,

        # input
        text_length,

        # output
        pto_p,
        pfr_p,
        emb_p
    )


    # Pythonizing the output

    output_u = _utf32_p_to_pyunicode(input_utf32_p)

    if with_position_to or with_position_from or with_embedding_level:
        res = (output_u, )
        if with_position_to:        res += ([i for i in pto_p], )
        if with_position_from:      res += ([i for i in pfr_p], )
        if with_embedding_level:    res += ([i for i in emb_p], )

    else:
        res = output_u

    return res


def get_mirror_chars(unicode_text):
    """
    Return TODO

    TODO.

    *  fribidi_get_mirror_char() returns the mirrored character, if input
    *  character has a mirror, or the input itself.
    *  if mirrored_ch is NULL, just returns if character has a mirror or not.
    """

    if not isinstance(unicode_text, unicode):
        unicode_text = unicode(unicode_text)

    res = UnicodeType()

    for unicode_char in unicode_text:
        text_length = len(unicode_text)

        # Memory allocations

        input_utf32_p = _pyunicode_to_utf32_p(unicode_char)

        output_utf32_p = _malloc.int32_array(text_length+1)

        # Calling the API

        """
        FRIBIDI_API fribidi_boolean fribidi_get_mirror_char (

            /* Input */
            FriBidiChar ch,

            /* Output */
            FriBidiChar *mirrored_ch
        );
        """

        _libfribidi.fribidi_get_mirror_char(
            # input
            input_utf32_p[0],
            # output
            output_utf32_p
        )

        # Pythonizing the output

        res += _utf32_p_to_pyunicode(output_utf32_p)

    return res


def get_mirror_prop(unicode_text):
    """
    Return TODO

    TODO.

    *  fribidi_get_mirror_char() returns the mirrored character, if input
    *  character has a mirror, or the input itself.
    *  if mirrored_ch is NULL, just returns if character has a mirror or not.
    """

    if not isinstance(unicode_text, unicode):
        unicode_text = unicode(unicode_text)

    res = []

    for unicode_char in unicode_text:

        # Memory allocations

        input_utf32_p = _pyunicode_to_utf32_p(unicode_char)

        # Calling the API

        """
        FRIBIDI_API fribidi_boolean fribidi_get_mirror_char (

            /* Input */
            FriBidiChar ch,

            /* Output */
            FriBidiChar *mirrored_ch
        );
        """

        is_mirror = _libfribidi.fribidi_get_mirror_char(
            # input
            input_utf32_p[0],
            # output
            None
        )

        # Pythonizing the output

        res.append(is_mirror)

    return res


def get_version_info():
    """
    Return TODO

    TODO.
    """

    # TODO

    return str(_libfribidi.fribidi_version_info)


# Main

def _main():
    """
    Print visual representation of command-line parameters (as a whole).
    """

    import sys
    text = ' '.join(sys.argv[1:]).decode('UTF-8')
    print(log2vis(text))


if __name__=='__main__':
    _main()

