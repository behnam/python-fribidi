#!/usr/bin/env python
# coding=UTF-8

import ctypes


VERSION = '0.08'

_libfribidi = ctypes.CDLL("libfribidi.so")


# Character Types

class types:
    """
    Defines character type masks and types.

    Types:

        LTR     Strong left to right
        RTL     Right to left characters
        AL      Arabic characters
        LRE     Left-To-Right embedding
        RLE     Right-To-Left embedding
        LRO     Left-To-Right override
        RLO     Right-To-Left override

        PDF     Pop directional override
        EN      European digit
        AN      Arabic digit
        ES      European number separator
        ET      European number terminator
        CS      Common Separator
        NSM     Non spacing mark
        BN      Boundary neutral

        BS      Block separator
        SS      Segment separator
        WS      Whitespace
        ON      Other Neutral

    Maskes:

        MASK_RTL        Is right to left
        MASK_ARABIC     Is arabic

    Each character can be only one of the three following:
        MASK_STRONG     Is strong
        MASK_WEAK       Is weak
        MASK_NEUTRAL    Is neutral

    Each charcter can be only one of the five following:
        MASK_LETTER     Is letter: L, R, AL
        MASK_NUMBER     Is number: EN, AN
        MASK_NUMSEPTER  Is number separator or terminator: ES, ET, CS
        MASK_SPACE      Is space: BN, BS, SS, WS
        MASK_EXPLICIT   Is expilict mark: LRE, RLE, LRO, RLO, PDF

        MASK_SEPARATOR  Is test separator: BS, SS; and can be on only if MASK_SPACE is also on.
        MASK_OVERRIDE   Is explicit override: LRO, RLO; and can be on only if MASK_EXPLICIT is also on.
    """

    # Define Masks

    MASK_RTL        = 0x00000001   # Is right to left
    MASK_ARABIC     = 0x00000002   # Is arabic

    MASK_STRONG     = 0x00000010   # Is strong
    MASK_WEAK       = 0x00000020   # Is weak
    MASK_NEUTRAL    = 0x00000040   # Is neutral

    MASK_LETTER     = 0x00000100   # Is letter: L, R, AL
    MASK_NUMBER     = 0x00000200   # Is number: EN, AN
    MASK_NUMSEPTER  = 0x00000400   # Is number separator or terminator: ES, ET, CS
    MASK_SPACE      = 0x00000800   # Is space: BN, BS, SS, WS
    MASK_EXPLICIT   = 0x00001000   # Is expilict mark: LRE, RLE, LRO, RLO, PDF

    MASK_SEPARATOR  = 0x00002000   # Is test separator: BS, SS

    MASK_OVERRIDE   = 0x00004000   # Is explicit override: LRO, RLO

    # The following must be to make types pairwise different, some of them can
    # be removed but are here because of efficiency (make queries faster).

    MASK_ES     = 0x00010000
    MASK_ET     = 0x00020000
    MASK_CS     = 0x00040000

    MASK_NSM    = 0x00080000
    MASK_BN     = 0x00100000

    MASK_BS     = 0x00200000
    MASK_SS     = 0x00400000
    MASK_WS     = 0x00800000

    # Define values for FriBidiCharType

    LTR     = (MASK_STRONG + MASK_LETTER)                               # Strong left to right
    RTL     = (MASK_STRONG + MASK_LETTER + MASK_RTL)                    # Right to left characters
    AL      = (MASK_STRONG + MASK_LETTER + MASK_RTL + MASK_ARABIC)      # Arabic characters
    LRE     = (MASK_STRONG + MASK_EXPLICIT)                             # Left-To-Right embedding
    RLE     = (MASK_STRONG + MASK_EXPLICIT + MASK_RTL)                  # Right-To-Left embedding
    LRO     = (MASK_STRONG + MASK_EXPLICIT + MASK_OVERRIDE)             # Left-To-Right override
    RLO     = (MASK_STRONG + MASK_EXPLICIT + MASK_RTL + MASK_OVERRIDE)  # Right-To-Left override

    PDF     = (MASK_WEAK + MASK_EXPLICIT)                               # Pop directional override
    EN      = (MASK_WEAK + MASK_NUMBER)                                 # European digit
    AN      = (MASK_WEAK + MASK_NUMBER + MASK_ARABIC)                   # Arabic digit
    ES      = (MASK_WEAK + MASK_NUMSEPTER + MASK_ES)                    # European number separator
    ET      = (MASK_WEAK + MASK_NUMSEPTER + MASK_ET)                    # European number terminator
    CS      = (MASK_WEAK + MASK_NUMSEPTER + MASK_CS)                    # Common Separator
    NSM     = (MASK_WEAK + MASK_NSM)                                    # Non spacing mark
    BN      = (MASK_WEAK + MASK_SPACE + MASK_BN)                        # Boundary neutral

    BS      = (MASK_NEUTRAL + MASK_SPACE + MASK_SEPARATOR + MASK_BS)    # Block separator
    SS      = (MASK_NEUTRAL + MASK_SPACE + MASK_SEPARATOR + MASK_SS)    # Segment separator
    WS      = (MASK_NEUTRAL + MASK_SPACE + MASK_WS)                     # Whitespace
    ON      = (MASK_NEUTRAL)                                            # Other Neutral


# Memory allocation functions


def _malloc_int_array (l):
    """
    Returns a pointer to allocated C int array of length `l'
    """

    t = ctypes.c_int * l
    return t()

def _malloc_int8_array (l):
    """
    Returns a pointer to allocated C int array of length `l'
    """

    t = ctypes.c_int8 * l
    return t()


def _malloc_utf8_array (l):
    """
    Returns a pointer to allocated UTF8 (C char) array of length `l'
    """

    t = ctypes.c_char * l
    return t()


def _malloc_utf8_array_from_string (s):
    """
    Returns a pointer to allocated UTF8 (C char) array, initialized with value of `s'
    """

    return ctypes.c_char_p(s)


def _malloc_utc32_array (l):
    """
    Returns a pointer to allocated UTC32 (C int32) array of length `l'
    """

    t = ctypes.c_uint32 * l
    return t()


# Unicode type convertors

def _pyunicode_to_utc32_p (a_pyunicode):
    """
    Converts Python Unicode instance to UTC32 (C int32) array
    """

    a_len = len(a_pyunicode)

    #print 'a_len', a_len

    utf8_pystr = a_pyunicode.encode('UTF-8')
    utf8_len = len(utf8_pystr)
    utf8_p = _malloc_utf8_array_from_string(utf8_pystr)

    #print 'utf8_p.value', utf8_p.value
    #print 'utf8_len', utf8_len

    utc32_p = _malloc_utc32_array(a_len+1)
    _libfribidi.fribidi_utf8_to_unicode (utf8_p, utf8_len, utc32_p)

    #print 'utc32_p [%04x, %04x, %04x, %04x]' % (utc32_p[0], utc32_p[1], utc32_p[2], utc32_p[3])

    # XX: Caller should free it!
    return utc32_p


def _utc32_p_to_pyunicode (a_utc32_p):
    """
    Converts UTC32 (C int32) array to Python Unicode instance
    """

    #print 'a_utc32_p [%04x, %04x, %04x, %04x]' % (a_utc32_p[0], a_utc32_p[1], a_utc32_p[2], a_utc32_p[3])

    utc32_len = ctypes.sizeof(a_utc32_p) / ctypes.sizeof(ctypes.c_uint32)
    #print 'utc32_len', utc32_len

    utf8_len = 6*utc32_len+1
    utf8_p = _malloc_utf8_array(utf8_len)

    _libfribidi.fribidi_unicode_to_utf8 (a_utc32_p, utc32_len, utf8_p)

    return utf8_p.value



# FriBidi API

def log2vis (unicode_text, base_direction, with_l2v_position=False, with_v2l_position=False, with_embedding_level=False):
    """
    Returns the visual order of characters in the text.

    If with_l2v_position, with_v2l_position, or with_embedding_level are
    True, the return value will be a tuple including logical-to-visual
    position, visual-to-logical positions, or embedding-level lists
    respectively.
    """

    if unicode_text.__class__ != unicode:
        unicode_text = unicode(unicode_text)

    input_len = len(unicode_text)

    # Memory allocations

    input_utc32_p = _pyunicode_to_utc32_p(unicode_text)
    pbase_dir_p = ctypes.pointer(ctypes.c_int32(base_direction))

    output_utc32_p = _malloc_utc32_array(input_len+1)

    l2v_p = _malloc_int_array(input_len)    if with_l2v_position    else None
    v2l_p = _malloc_int_array(input_len)    if with_v2l_position    else None
    emb_p = _malloc_int8_array(input_len)   if with_embedding_level else None


    # Calling the api

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
        input_utc32_p,
        input_len,
        pbase_dir_p,

        # output
        output_utc32_p,
        l2v_p,
        v2l_p,
        emb_p
    )

    if not successed:
        raise Exception('fribidi_log2vis failed')


    # Pythonizing the output

    output_u = _utc32_p_to_pyunicode(output_utc32_p)

    if with_l2v_position or with_v2l_position or with_embedding_level:
        res = (output_u, )
        if with_l2v_position:       res += ([i for i in l2v_p], )
        if with_v2l_position:       res += ([i for i in v2l_p], )
        if with_embedding_level:    res += ([i for i in emb_p], )

    else:
        res = output_u

    return res


def log2vis_get_embedding_levels (unicode_text, base_direction):
    """
    Returns the embedding-level of characters in the text.
    """

    if unicode_text.__class__ != unicode:
        unicode_text = unicode(unicode_text)

    input_len = len(unicode_text)

    # Memory allocations

    input_utc32_p = _pyunicode_to_utc32_p(unicode_text)
    pbase_dir_p = ctypes.pointer(ctypes.c_int32(base_direction))

    emb_p = _malloc_int8_array(input_len)


    # Calling the api

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
        input_utc32_p,
        input_len,
        pbase_dir_p,

        # output
        emb_p
    )

    if not successed:
        raise Exception('fribidi_log2vis_get_embedding_levels failed')


    # Pythonizing the output

    res = [i for i in emb_p]

    return res


def remove_bidi_marks (unicode_text, with_position_to=False, with_position_from=False, with_embedding_level=False):
    """
    Returns the text with all Bidirectional Marks removed.

    If with_position_to, with_position_from, or with_embedding_level are
    True, the return value will be a tuple including positions from
    input text to output text, positions from output text to input text,
    or embedding-level lists respectively.
    """

    if unicode_text.__class__ != unicode:
        unicode_text = unicode(unicode_text)

    input_len = len(unicode_text)


    # Memory allocations

    input_utc32_p = _pyunicode_to_utc32_p(unicode_text)

    pto_p = _malloc_int_array(input_len*3)    if with_position_to     else None
    pfr_p = _malloc_int_array(input_len)    if with_position_from   else None
    emb_p = _malloc_int8_array(input_len)   if with_embedding_level else None
    #print 'pto_p', pto_p


    # Calling the api

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
        input_utc32_p,

        # input
        input_len,

        # output
        pto_p,
        pfr_p,
        emb_p
    )


    # Pythonizing the output

    output_u = _utc32_p_to_pyunicode(input_utc32_p)

    if with_position_to or with_position_from or with_embedding_level:
        res = (output_u, )
        if with_position_to:        res += ([i for i in pto_p], )
        if with_position_from:      res += ([i for i in pfr_p], )
        if with_embedding_level:    res += ([i for i in emb_p], )

    else:
        res = output_u

    return res


# Main

def _main ():
    import sys
    text = ' '.join(sys.argv[1:]).decode('UTF-8')
    print log2vis(text, types.LTR)


def _test ():

    print
    print 'TEST log2vis()'

    print log2vis(u"سلام", types.LTR)
    print log2vis(u"سلام", types.LTR, True)
    print log2vis(u"سلام", types.LTR, False, True)
    print log2vis(u"سلام", types.LTR, False, False, True)

    print log2vis(u"سلام", types.LTR, True, True, True)
    print log2vis(u"سلام", types.RTL, True, True, True)

    print log2vis(u"1سلام", types.LTR, True, True, True)
    print log2vis(u"1سلام", types.RTL, True, True, True)

    print log2vis(u"aسلام", types.LTR, True, True, True)
    print log2vis(u"aسلام", types.RTL, True, True, True)

    print
    print 'TEST log2vis_get_embedding_levels()'

    print log2vis_get_embedding_levels("abc", types.LTR)
    print log2vis_get_embedding_levels(u"aسلام", types.LTR)
    print log2vis_get_embedding_levels(u"aسلام", types.RTL)

    print
    print 'TEST remove_bidi_marks()'

    print remove_bidi_marks(u"سلامa")
    print remove_bidi_marks(u"سلامa", False, True)
    print remove_bidi_marks(u"سلامa", False, False, True)
    print remove_bidi_marks(u"سلامa", True)

    print remove_bidi_marks(u"سل‌ام")
    print remove_bidi_marks(u"سل‌ام", True)
    print remove_bidi_marks(u"سل‌ام", False, True)
    print remove_bidi_marks(u"سل‌ام", False, False, True)


if __name__=='__main__':
    _main()

    _test()

