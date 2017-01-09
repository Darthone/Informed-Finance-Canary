import datetime
import sys
import inspect
import json

if sys.version_info < (2, 7):
    from unittest2 import main as test_main, SkipTest, TestCase
else:
    from unittest import main as test_main, SkipTest, TestCase

from yahoo_finance import Share, get_date_range
from pprint import pprint

class TestShare(TestCase):
	
	def test_get_historical(self):
		# Stock ticker
		ticker = 'F'
		# Format: YYYY-MM-DD 
		begin_date = '2012-04-25'
		end_date = '2014-04-29'
		file_name = ticker + "_" + begin_date + "_" + end_date
		self.stock = Share(ticker)
		history = self.stock.get_historical(begin_date,end_date)
		with open('%s.txt' %file_name, 'wb') as outfile:
			json.dump(history,outfile,sort_keys=True, indent=4, separators=(',', ': '))
		#pprint(history)
		
if __name__ == "__main__":
    test_main()
