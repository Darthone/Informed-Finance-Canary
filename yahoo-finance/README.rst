=============
yahoo-finance
=============

Python module to get stock data from Yahoo! Finance

Yahoo! Finance backend is http://datatables.org/. If this service is down or
has network problems you will receive errors from group YQL*,
eg. ``YQLQueryError``.

You can monitor this service via https://www.datatables.org/healthchecker/

More details https://github.com/lukaszbanasiak/yahoo-finance/issues/44

Usage
-------
    Install venv and activate
    
    Run python setup.py install
    
    Run python test/test_stocks.py

Usage examples
--------------

Get shares data
^^^^^^^^^^^^^^^

Example: Yahoo! Inc. (``YHOO``)

.. code:: python

    >>> from yahoo_finance import Share
    >>> yahoo = Share('YHOO')
    >>> print yahoo.get_open()
    '36.60'
    >>> print yahoo.get_price()
    '36.84'
    >>> print yahoo.get_trade_datetime()
    '2014-02-05 20:50:00 UTC+0000'

Refresh data from market

.. code:: python

    >>> yahoo.refresh()
    >>> print yahoo.get_price()
    '36.87'
    >>> print yahoo.get_trade_datetime()
    '2014-02-05 21:00:00 UTC+0000'

Historical data

.. code:: python

    >>> print yahoo.get_historical('2014-04-25', '2014-04-29')
    [{u'Volume': u'28720000', u'Symbol': u'YHOO', u'Adj_Close': u'35.83', u'High': u'35.89', u'Low': u'34.12', u'Date': u'2014-04-29', u'Close': u'35.83', u'Open': u'34.37'}, {u'Volume': u'30422000', u'Symbol': u'YHOO', u'Adj_Close': u'33.99', u'High': u'35.00', u'Low': u'33.65', u'Date': u'2014-04-28', u'Close': u'33.99', u'Open': u'34.67'}, {u'Volume': u'19391100', u'Symbol': u'YHOO', u'Adj_Close': u'34.48', u'High': u'35.10', u'Low': u'34.29', u'Date': u'2014-04-25', u'Close': u'34.48', u'Open': u'35.03'}]

More readable output :)

.. code:: python

    >>> from pprint import pprint
    >>> pprint(yahoo.get_historical('2014-04-25', '2014-04-29'))
    [{u'Adj_Close': u'35.83',
      u'Close': u'35.83',
      u'Date': u'2014-04-29',
      u'High': u'35.89',
      u'Low': u'34.12',
      u'Open': u'34.37',
      u'Symbol': u'YHOO',
      u'Volume': u'28720000'},
     {u'Adj_Close': u'33.99',
      u'Close': u'33.99',
      u'Date': u'2014-04-28',
      u'High': u'35.00',
      u'Low': u'33.65',
      u'Open': u'34.67',
      u'Symbol': u'YHOO',
      u'Volume': u'30422000'},
     {u'Adj_Close': u'34.48',
      u'Close': u'34.48',
      u'Date': u'2014-04-25',
      u'High': u'35.10',
      u'Low': u'34.29',
      u'Open': u'35.03',
      u'Symbol': u'YHOO',
      u'Volume': u'19391100'}]

Available methods

- ``get_price()``
- ``get_change()``
- ``get_percent_change()``
- ``get_volume()``
- ``get_prev_close()``
- ``get_open()``
- ``get_avg_daily_volume()``
- ``get_stock_exchange()``
- ``get_market_cap()``
- ``get_book_value()``
- ``get_ebitda()``
- ``get_dividend_share()``
- ``get_dividend_yield()``
- ``get_earnings_share()``
- ``get_days_high()``
- ``get_days_low()``
- ``get_year_high()``
- ``get_year_low()``
- ``get_50day_moving_avg()``
- ``get_200day_moving_avg()``
- ``get_price_earnings_ratio()``
- ``get_price_earnings_growth_ratio()``
- ``get_price_sales()``
- ``get_price_book()``
- ``get_short_ratio()``
- ``get_trade_datetime()``
- ``get_historical(start_date, end_date)``
- ``get_name()``
- ``refresh()``
- ``get_percent_change_from_year_high()``
- ``get_percent_change_from_year_low()``
- ``get_change_from_year_low()``
- ``get_change_from_year_high()``
- ``get_percent_change_from_200_day_moving_average()``
- ``get_change_from_200_day_moving_average()``
- ``get_percent_change_from_50_day_moving_average()``
- ``get_change_from_50_day_moving_average()``
- ``get_EPS_estimate_next_quarter()``
- ``get_EPS_estimate_next_year()``
- ``get_ex_dividend_date()``
- ``get_EPS_estimate_current_year()``
- ``get_price_EPS_estimate_next_year()``
- ``get_price_EPS_estimate_current_year()``
- ``get_one_yr_target_price()``
- ``get_change_percent_change()``
- ``get_dividend_pay_date()``
- ``get_currency()``
- ``get_last_trade_with_time()``
- ``get_days_range()``
- ``get_year_range()``

Requirements
------------

See ``requirements.txt``
