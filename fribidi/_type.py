# coding=UTF-8

# TODO: COPYRIGHT

# ########################################################################
# FriBidi API, Bidi, Types (fribidi-bidi-types.h)

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


# Mask and Type functions

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

