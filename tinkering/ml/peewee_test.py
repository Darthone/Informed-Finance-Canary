#!/usr/bin/env python
#import peewee as pw
#from peewee import *
#from ifc.ta import get_series
import ifc.ta as ta
#database = MySQLDatabase("ifc", host="192.168.1.128", port=3306, user="", passwd="")
print dir(ta)
x = ta.get_series("TGT", "2015-04-17", "2016-04-17")
x.run_calculations()                            
x.trim_fat()                                    
print x.df


