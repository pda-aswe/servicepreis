from src import messenger
from unittest.mock import patch, ANY, MagicMock
import json

@patch("stock.Stock")
def test_connect(mock_stock):
    obj = messenger.Messenger()

    with patch.object(obj, 'mqttConnection') as mock_connect:
        obj.connect()
        mock_connect.connect.assert_called_with("localhost",1883,60)

@patch("stock.Stock")
def test_disconnect(mock_stock):
    obj = messenger.Messenger()

    with patch.object(obj, 'connected', True), patch.object(obj, 'mqttConnection') as mock_connect:
        obj.disconnect()
        mock_connect.disconnect.assert_called()

@patch("stock.Stock")
def test_foreverLoop(mock_stock):
    obj = messenger.Messenger()

    with patch.object(obj, 'mqttConnection') as mock_connect:
        obj.foreverLoop()
        mock_connect.loop_forever.assert_called()

@patch("stock.Stock")
def test_onMQTTconnect(mock_stock):
    obj = messenger.Messenger()

    mock_client = MagicMock()

    obj._Messenger__onMQTTconnect(mock_client,None,None,None)

    mock_client.subscribe.assert_called_with([('req/price', 0)])


@patch("stock.Stock")
def test_onMQTTMessage(mock_stock):
    obj = messenger.Messenger()

    obj._Messenger__onMQTTMessage(MagicMock(),None,None)

class DummyMSG:
    def __init__(self):
        self.payload = "Test"

    def set_payload(self,data):
        self.payload = str.encode(data)

@patch("stock.Stock")
def test_mailMQTTRideTimecallback(mock_stock):
    obj = messenger.Messenger()

    responseData = DummyMSG()

    msgData = {
       "symbol":"aapl"
    }

    responseData.set_payload(json.dumps(msgData))

    with patch.object(obj, 'stockService') as mockStock, patch.object(obj,'mqttConnection') as mockConnection:
        mockStock.getStockPrice.return_value = {'symbol':'aapl','current':0.0,'highestDay':0.0,'lowestDay':0.0,'timestamp':0}
        obj._Messenger__mailMQTTPricecallback(None,None,responseData)
        mockStock.getStockPrice.assert_called_with("aapl")
        mockConnection.publish.assert_called_with("price/current",json.dumps({'symbol':'aapl','current':0.0,'highestDay':0.0,'lowestDay':0.0,'timestamp':0}))