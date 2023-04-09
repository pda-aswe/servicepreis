from src import messenger
from unittest.mock import patch, ANY, MagicMock
import json

@patch("travel.Travel")
def test_connect(mock_travel):
    obj = messenger.Messenger()

    with patch.object(obj, 'mqttConnection') as mock_connect:
        obj.connect()
        mock_connect.connect.assert_called_with("localhost",1883,60)

@patch("travel.Travel")
def test_disconnect(mock_travel):
    obj = messenger.Messenger()

    with patch.object(obj, 'connected', True), patch.object(obj, 'mqttConnection') as mock_connect:
        obj.disconnect()
        mock_connect.disconnect.assert_called()

@patch("travel.Travel")
def test_foreverLoop(mock_travel):
    obj = messenger.Messenger()

    with patch.object(obj, 'mqttConnection') as mock_connect:
        obj.foreverLoop()
        mock_connect.loop_forever.assert_called()

@patch("travel.Travel")
def test_onMQTTconnect(mock_travel):
    obj = messenger.Messenger()

    mock_client = MagicMock()

    obj._Messenger__onMQTTconnect(mock_client,None,None,None)

    mock_client.subscribe.assert_called_with([('req/rideTime', 0)])


@patch("travel.Travel")
def test_onMQTTMessage(mock_travel):
    obj = messenger.Messenger()

    obj._Messenger__onMQTTMessage(MagicMock(),None,None)

class DummyMSG:
    def __init__(self):
        self.payload = "Test"

    def set_payload(self,data):
        self.payload = str.encode(data)

@patch("travel.Travel")
def test_mailMQTTRideTimecallback(mock_travel):
    obj = messenger.Messenger()

    responseData = DummyMSG()

    msgData = {
    "from":{
        "lat" : 0.0,
        "lon" : 0.0
    },
    "to":{
        "lat" : 0.0,
        "lon" : 0.0
    },
        "transportType":"car"
    }

    responseData.set_payload(json.dumps(msgData))

    with patch.object(obj, 'travelService') as mock_travel:
        mock_travel.travelTimeCar.return_value = 10
        obj._Messenger__mailMQTTRideTimecallback(None,None,responseData)
        mock_travel.travelTimeCar.assert_called_with({'lat': 0.0, 'lon': 0.0}, {'lat': 0.0, 'lon': 0.0})