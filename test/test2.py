#!/usr/bin/env python
# coding=UTF-8


from fribidi import *

s = u'سلام ABC'

print 'ORIG\t%s' % s
print 'LTR\t%s' % log2vis(s, None, ParType.LTR)
print 'RTL\t%s' % log2vis(s, None, ParType.RTL)

s = u'46/12/2008'

print 'ORIG\t%s' % s
print 'LTR\t%s' % log2vis(s, None, ParType.LTR)
print 'RTL\t%s' % log2vis(s, None, ParType.RTL)

s = u'٤٦/١٢/٢٠٠٨'

print 'ORIG\t%s' % s
print 'LTR\t%s' % log2vis(s, None, ParType.LTR)
print 'RTL\t%s' % log2vis(s, None, ParType.RTL)

s = u'۴۶/۱۲/۲۰۰۸'

print 'ORIG\t%s' % s
print 'LTR\t%s' % log2vis(s, None, ParType.LTR)
print 'RTL\t%s' % log2vis(s, None, ParType.RTL)

