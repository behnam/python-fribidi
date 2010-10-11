#!/usr/bin/env python
# coding=UTF-8


from fribidi.fribidi import *

s = u'سلام ABC'

print u'ORIG\t%s' % s
print u'LTR\t%s' % log2vis(s, None, ParType.LTR)
print u'RTL\t%s' % log2vis(s, None, ParType.RTL)

s = u'46/12/2008'

print u'ORIG\t%s' % s
print u'LTR\t%s' % log2vis(s, None, ParType.LTR)
print u'RTL\t%s' % log2vis(s, None, ParType.RTL)

s = u'٤٦/١٢/٢٠٠٨'

print u'ORIG\t%s' % s
print u'LTR\t%s' % log2vis(s, None, ParType.LTR)
print u'RTL\t%s' % log2vis(s, None, ParType.RTL)

s = u'۴۶/۱۲/۲۰۰۸'

print u'ORIG\t%s' % s
print u'LTR\t%s' % log2vis(s, None, ParType.LTR)
print u'RTL\t%s' % log2vis(s, None, ParType.RTL)

# vim:set encoding=utf-8:
