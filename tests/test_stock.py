from src import stock
from unittest.mock import patch, ANY, mock_open

@patch('builtins.open', new_callable=mock_open, read_data='test')
@patch("os.path.exists")
def test_loadAPIKey(mock_exists,mock_open):
    obj = stock.Stock()

    string_read = obj._Stock__loadAPIKey()
    assert string_read == "test"

@patch("builtins.open")
@patch("os.path.exists")
def test_getStockPrice(mock_exists,mock_open):
    obj = stock.Stock()

    with patch.object(obj,"finnhub_client") as mockFinnhub:
        mockFinnhub.quote.return_value = {}
        obj.getStockPrice("aapl")
        mockFinnhub.quote.assert_called_with('aapl')