#!/usr/bin/env python

from ifc import stockData, ta

raw_data = stockData.get_data_for_sym('AAPL', '2017-02-11', '2017-02-21')
my_series = ta.dicts_to_series(raw_data)
for day in my_series:
    print day.date, day.open

