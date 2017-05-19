#!/usr/bin/env python
#import peewee as pw
#from peewee import *
#from ifc.ta import get_series
import ifc.ta as ta
print dir(ta)
x = ta.get_series("TGT", "2016-04-17", "2017-04-17")
x.run_calculations()                            
x.trim_fat()                                    
print x.df


