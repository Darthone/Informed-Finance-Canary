
from ifc import articles

def test_get_tickers():
    ticker = "AAPL.O"
    test_str = "foo bar baz (%s)" % (ticker)
    res = articles.find_stock_tickers(test_str)
    assert len(res) == 1 and res[0] == ticker
 
