#!/usr/bin/env python
# coding=UTF-8

"""
an implementation of Unicode Bidirectional Algorithm, using GNU FriBidi

This is a python wrap of GNU FriBidi C library.
http://fribidi.org/

GNU FriBidi is an implementation of Unicode Bidirectional Algorithm (bidi).
http://unicode.org/reports/tr9/

"""


import ctypes


# Load FriBidi

_libfribidi = ctypes.CDLL("libfribidi.so")

try:
    _libfribidi.fribidi_shape()
except AttributeError:
    libfribidi_version = '0.10'
    libfribidi_version_major = 0
    libfribidi_version_minor = 10
else:
    libfribidi_version = '0.19'
    libfribidi_version_major = 0
    libfribidi_version_minor = 19

print libfribidi_version, libfribidi_version_major, libfribidi_version_minor


# Versions

VERSION = '0.10'
"Version of the python wrapper."


# Memory allocation functions

def _malloc_int_array(n):

    """Return a pointer to allocated C int array of length `n'.
    """

    t = ctypes.c_int * n
    return t()


def _malloc_int8_array(n):

    """Return a pointer to allocated C int array of length `n'.
    """

    t = ctypes.c_int8 * n
    return t()


def _malloc_int32_array(n):

    """Return a pointer to allocated UTF32 (C int32) array of length `n'.
    """

    t = ctypes.c_uint32 * n
    return t()


def _malloc_char_array(n):

    """Return a pointer to allocated UTF8 (C char) array of length `n'.
    """

    t = ctypes.c_char * n
    return t()


def _malloc_char_array_from_string(s):

    """Return a pointer to allocated UTF8 (C char) array, initialized with `s'.
    """

    return ctypes.c_char_p(s)


# Unicode type convertors

def _pyunicode_to_utf32_p(a_pyunicode):
    """Return UTF32 (C int32) array from Py_Unicode.
    """

    a_len = len(a_pyunicode)

    utf8_pystr = a_pyunicode.encode('UTF-8')
    utf8_len = len(utf8_pystr)
    utf8_p = _malloc_char_array_from_string(utf8_pystr)

    utf32_p = _malloc_int32_array(a_len+1)
    _libfribidi.fribidi_utf8_to_unicode(utf8_p, utf8_len, utf32_p)

    return utf32_p


def _utf32_p_to_pyunicode(a_utf32_p):
    """Return Py_Unicode from UTF32 (C int32) array.
    """

    utf32_len = ctypes.sizeof(a_utf32_p) / ctypes.sizeof(ctypes.c_uint32)

    utf8_len = 6*utf32_len+1
    utf8_p = _malloc_char_array(utf8_len)

    _libfribidi.fribidi_unicode_to_utf8(a_utf32_p, utf32_len, utf8_p)

    return utf8_p.value.decode('UTF-8')



# Character and Paragraph Masks and Types

class Mask:
    """
    TODO.
    """

    # Mask values

    RTL         = 0x00000001    # Is right to left
    ARABIC      = 0x00000002    # Is arabic

    # Each character can be only one of the three following:
    STRONG      = 0x00000010    # Is strong
    WEAK        = 0x00000020    # Is weak
    NEUTRAL     = 0x00000040    # Is neutral
    SENTINEL    = 0x00000080    # Is sentinel
    # Sentinels are not valid chars, just identify the start/end of strings.

    # Each charcter can be only one of the five following:
    LETTER      = 0x00000100    # Is letter: L, R, AL
    NUMBER      = 0x00000200    # Is number: EN, AN
    NUMSEPTER   = 0x00000400    # Is number separator or terminator: ES, ET, CS
    SPACE       = 0x00000800    # Is space: BN, BS, SS, WS
    EXPLICIT    = 0x00001000    # Is expilict mark: LRE, RLE, LRO, RLO, PDF

    # Can be set only if Mask.SPACE is also set.
    SEPARATOR   = 0x00002000    # Is test separator: BS, SS

    OVERRIDE    = 0x00004000    # Is explicit override: LRO, RLO

    # The following must be to make types pairwise different, some of them can
    # be removed but are here because of efficiency (make queries faster).
    ES          = 0x00010000
    ET          = 0x00020000
    CS          = 0x00040000

    NSM         = 0x00080000
    BN          = 0x00100000

    BS          = 0x00200000
    SS          = 0x00400000
    WS          = 0x00800000

    # We reserve a single bit for user's private use: we will never use it.
    PRIVATE     = 0x01000000


class _Type:
    """
    TODO.
    """

    # Strong types

    LTR     = Mask.STRONG + Mask.LETTER                                 # Left-To-Right letter
    RTL     = Mask.STRONG + Mask.LETTER + Mask.RTL                      # Right-To-Left letter
    AL      = Mask.STRONG + Mask.LETTER + Mask.RTL + Mask.ARABIC        # Arabic Letter
    LRE     = Mask.STRONG + Mask.EXPLICIT                               # Left-to-Right Embedding
    RLE     = Mask.STRONG + Mask.EXPLICIT + Mask.RTL                    # Right-to-Left Embedding
    LRO     = Mask.STRONG + Mask.EXPLICIT + Mask.OVERRIDE               # Left-to-Right Override
    RLO     = Mask.STRONG + Mask.EXPLICIT + Mask.RTL + Mask.OVERRIDE    # Right-to-Left Override

    # Weak types

    PDF     = Mask.WEAK + Mask.EXPLICIT                                 # Pop Directional Override
    EN      = Mask.WEAK + Mask.NUMBER                                   # European Numeral
    AN      = Mask.WEAK + Mask.NUMBER + Mask.ARABIC                     # Arabic Numeral
    ES      = Mask.WEAK + Mask.NUMSEPTER + Mask.ES                      # European number Separator
    ET      = Mask.WEAK + Mask.NUMSEPTER + Mask.ET                      # European number Terminator
    CS      = Mask.WEAK + Mask.NUMSEPTER + Mask.CS                      # Common Separator
    NSM     = Mask.WEAK + Mask.NSM                                      # Non Spacing Mark
    BN      = Mask.WEAK + Mask.SPACE + Mask.BN                          # Boundary Neutral

    # Neutral types

    BS      = Mask.NEUTRAL + Mask.SPACE + Mask.SEPARATOR + Mask.BS      # Block Separator
    SS      = Mask.NEUTRAL + Mask.SPACE + Mask.SEPARATOR + Mask.SS      # Segment Separator
    WS      = Mask.NEUTRAL + Mask.SPACE + Mask.WS                       # WhiteSpace
    ON      = Mask.NEUTRAL                                              # Other Neutral

    # Paragraph-only types

    WLTR        = Mask.WEAK             # Weak Left-To-Right
    WRTL        = Mask.WEAK | Mask.RTL  # Weak Right-To-Left

    SENTINEL    = Mask.SENTINEL         # start or end of text (run list) SENTINEL
                                        # Only used internally

    PRIVATE     = Mask.PRIVATE          # Private types for applications
                                        # More private types can be obtained by summing up from this one


class CharType:
    """
    Class of character (direction) types.

    Strong types:

        LTR     Left-To-Right letter
        RTL     Right-To-Left letter
        AL      Arabic Letter
        LRE     Left-to-Right Embedding
        RLE     Right-to-Left Embedding
        LRO     Left-to-Right Override
        RLO     Right-to-Left Override

    Weak types:

        PDF     Pop Directional Override
        EN      European Numeral
        AN      Arabic Numeral
        ES      European number Separator
        ET      European number Terminator
        CS      Common Separator
        NSM     Non Spacing Mark
        BN      Boundary Neutral

    Neutral types:

        BS      Block Separator
        SS      Segment Separator
        WS      WhiteSpace
        ON      Other Neutral

    """

    LTR = _Type.LTR
    RTL = _Type.RTL
    AL  = _Type.AL
    EN  = _Type.EN
    AN  = _Type.AN
    ES  = _Type.ES
    ET  = _Type.ET
    CS  = _Type.CS
    NSM = _Type.NSM
    BN  = _Type.BN
    BS  = _Type.BS
    SS  = _Type.SS
    WS  = _Type.WS
    ON  = _Type.ON
    LRE = _Type.LRE
    RLE = _Type.RLE
    LRO = _Type.LRO
    RLO = _Type.RLO
    PDF = _Type.PDF


class ParType:

    """
    Class of paragraph (direction) types:

        LTR     Left-to-Right paragraph
        RTL     Right-to-Left paragraph
        ON      (Other) Neutral paragraph
        WLTR    Weak Left-to-Right paragraph
        WRTL    Weak Right-to-Left paragraph

    """

    LTR     = _Type.LTR
    RTL     = _Type.RTL
    ON      = _Type.ON
    WLTR    = _Type.WLTR
    WRTL    = _Type.WRTL


# FriBidi API, Bidi part

def level_is_rtl(lev):

    """
    Return True if `lev' is a Right-to-Left level, False otherwise.

    """

    return lev & 1


def level_to_dir(lev):

    """
    Return the bidi type corresponding to the direction of the level number.

    Return ParType.LTR for evens, and ParType.RTL for odds.

    """

    return ParType.RTL if level_is_rtl(lev) else ParType.LTR


def dir_is_rtl(dir):

    """
    Return True if `dir' is a Right-to-Left, False otherwise.

    """

    return dir & Mask.RTL


def dir_to_level(dir):

    """
    Return the minimum level of the direction.

    Return 0 for LTR and 1 for RTL.

    """
     
    return 1 if dir_is_rtl(dir) else 0


# FriBidi API, Misc

def log2vis(unicode_text, base_direction=None, with_l2v_position=False, with_v2l_position=False, with_embedding_level=False):
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

    if base_direction is None:
        base_direction=ParType.LTR

    text_len = len(unicode_text)

    # Memory allocations

    input_utf32_p = _pyunicode_to_utf32_p(unicode_text)
    pbase_dir_p = ctypes.pointer(ctypes.c_int32(base_direction))

    output_utf32_p = _malloc_int32_array(text_len+1)

    l2v_p = _malloc_int_array(text_len)     if with_l2v_position    else None
    v2l_p = _malloc_int_array(text_len)     if with_v2l_position    else None
    emb_p = _malloc_int8_array(text_len)    if with_embedding_level else None

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
        text_len,
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

    emb_p = _malloc_int8_array(text_len)

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


def remove_bidi_marks(unicode_text, with_position_to=False, with_position_from=False, with_embedding_level=False):

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

    text_len = len(unicode_text)

    # Memory allocations

    input_utf32_p = _pyunicode_to_utf32_p(unicode_text)

    pto_p = _malloc_int_array(text_len)     if with_position_to     else None
    pfr_p = _malloc_int_array(text_len)     if with_position_from   else None
    emb_p = _malloc_int8_array(text_len)    if with_embedding_level else None

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
        text_len,

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


def get_types(unicode_text):

    """
    Return TODO

    TODO.
    """

    if not isinstance(unicode_text, unicode):
        unicode_text = unicode(unicode_text)

    text_len = len(unicode_text)

    # Memory allocations

    input_utf32_p = _pyunicode_to_utf32_p(unicode_text)

    output_chartype_p = _malloc_int32_array(text_len)

    # Calling the API

    """
    FRIBIDI_API void fribidi_get_types (

        /* input */
        FriBidiChar *str,
        FriBidiStrIndex len,

        /* output */
        FriBidiCharType *type
    );
    """

    _libfribidi.fribidi_get_types(
        # input
        input_utf32_p,
        text_len,
        output_chartype_p
    )

    # Pythonizing the output

    return [i for i in output_chartype_p]


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

    res = u''

    for unicode_char in unicode_text:
        text_len = len(unicode_text)

        # Memory allocations

        input_utf32_p = _pyunicode_to_utf32_p(unicode_char)

        output_utf32_p = _malloc_int32_array(text_len+1)

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
        text_len = len(unicode_text)

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
    Return visual text of command-line parameters (as a whole).

    """

    import sys
    text = ' '.join(sys.argv[1:]).decode('UTF-8')
    print log2vis(text)


def _test():

    print
    print 'Loaded: %s' % _libfribidi
    print

    print
    print 'TEST log2vis()'
    print

    print log2vis(123)
    print log2vis(u"سل‌ام")
    print log2vis(u"سل‌ام").__class__
    print

    print log2vis(u"سلام", None, True)
    print log2vis(u"سلام", None, False, True)
    print log2vis(u"سلام", None, False, False, True)

    print log2vis(u"1سلام", ParType.LTR, True, True, True)
    print log2vis(u"1سلام", ParType.RTL, True, True, True)

    print log2vis(u"aسلام", ParType.LTR, True, True, True)
    print log2vis(u"aسلام", ParType.RTL, True, True, True)

    print
    print 'TEST log2vis_get_embedding_levels()'
    print

    print log2vis_get_embedding_levels(123)
    print log2vis_get_embedding_levels(u"سل‌ام")
    print log2vis_get_embedding_levels(u"سل‌ام").__class__
    print

    print log2vis_get_embedding_levels("abc", ParType.LTR)
    print log2vis_get_embedding_levels(u"aسلام", ParType.LTR)
    print log2vis_get_embedding_levels(u"aسلام", ParType.RTL)

    print
    print 'TEST remove_bidi_marks()'
    print

    print remove_bidi_marks(123)
    print remove_bidi_marks(u"سل‌ام")
    print remove_bidi_marks(u"سل‌ام").__class__
    print

    print remove_bidi_marks(u"سلامa")
    #print remove_bidi_marks(u"سلامa", False, True)
    #print remove_bidi_marks(u"سلامa", False, False, True)
    #print remove_bidi_marks(u"سلامa", True)

    print remove_bidi_marks(u"سل‌ام")
    #print remove_bidi_marks(u"سل‌ام", True)
    #print remove_bidi_marks(u"سل‌ام", False, True)
    #print remove_bidi_marks(u"سل‌ام", False, False, True)

    if libfribidi_version_major == 1:
        print
        print 'TEST get_types()'
        print

        print get_types(123)
        print get_types(u"سل‌ام")
        print get_types(u"سل‌ام").__class__
        print

    print
    print 'TEST get_mirror_chars()'
    print

    print get_mirror_chars(123)
    print get_mirror_chars(u"سل‌ام")
    print get_mirror_chars(u"سل‌ام").__class__
    print

    a="()"; print a, get_mirror_chars(a)
    a=u"«»"; print a, get_mirror_chars(a)
    a=u"﴾﴿"; print a, get_mirror_chars(a)

    print
    print 'TEST get_mirror_prop()'
    print

    print get_mirror_prop(123)
    print get_mirror_prop(u"سل‌ام")
    print get_mirror_prop(u"سل‌ام").__class__
    print

    print u"() «» ﴾﴿", get_mirror_prop(u"() «» ﴾﴿")

    print
    print 'TEST get_version_info()'
    print

    print get_version_info()

if __name__=='__main__':
    _main()

    _test()

