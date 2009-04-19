#!/usr/bin/env python
# coding=UTF-8


from fribidi import *


def _main():

    print 'libfribidi version:', libfribidi_version, libfribidi_version_major, libfribidi_version_minor
    print

    # Bidi API

    print
    print 'TEST get_bidi_types()'
    print

    print get_bidi_types(123)
    print get_bidi_types(u"سل‌ام")
    print get_bidi_types(u"سل‌ام").__class__
    print

    print
    print 'TEST get_par_direction()'
    print

    print get_par_direction(get_bidi_types(123))
    print get_par_direction(get_bidi_types(u"سل‌ام"))
    print get_par_direction(get_bidi_types(u"سل‌ام")).__class__
    print

    print
    print 'TEST get_par_embedding_levels()'
    print

    print get_par_embedding_levels(get_bidi_types(123))
    print get_par_embedding_levels(get_bidi_types(u"سل‌ام"))
    print get_par_embedding_levels(get_bidi_types(u"سل‌ام")).__class__
    print

    print get_par_embedding_levels(get_bidi_types("abc"), None, ParType.LTR)
    print get_par_embedding_levels(get_bidi_types(u"aسلام"), None, ParType.LTR)
    print get_par_embedding_levels(get_bidi_types(u"aسلام"), None, ParType.RTL)

    '''
    print
    print 'TEST remove_bidi_marks()'
    print

    print remove_bidi_marks(123)
    print remove_bidi_marks(u"سل‌ام")
    print remove_bidi_marks(u"سل‌ام").__class__
    print

    print remove_bidi_marks(u"سلامa")
    #print remove_bidi_marks(u"سلامa", None, False, True)
    #print remove_bidi_marks(u"سلامa", None, False, False, True)
    #print remove_bidi_marks(u"سلامa", None, True)

    print remove_bidi_marks(u"سل‌ام")
    #print remove_bidi_marks(u"سل‌ام", None, True)
    #print remove_bidi_marks(u"سل‌ام", None, False, True)
    #print remove_bidi_marks(u"سل‌ام", None, False, False, True)

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

    print 'TEST log2vis()'
    print

    print log2vis(123)
    print log2vis(u"سل‌ام")
    print log2vis(u"سل‌ام").__class__
    print

    print log2vis(u"سلام", None, None, True)
    print log2vis(u"سلام", None, None, False, True)
    print log2vis(u"سلام", None, None, False, False, True)

    print log2vis(u"1سلام", None, ParType.LTR, True, True, True)
    print log2vis(u"1سلام", None, ParType.RTL, True, True, True)

    print log2vis(u"aسلام", None, ParType.LTR, True, True, True)
    print log2vis(u"aسلام", None, ParType.RTL, True, True, True)
    '''

if __name__ == '__main__':
    _main()

