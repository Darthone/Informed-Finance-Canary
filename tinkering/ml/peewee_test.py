import peewee as pw
from peewee import *

database = MySQLDatabase("ifc", host="192.168.1.128", port=3306, user="", passwd="")


query = stockfeature.select()
