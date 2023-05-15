import unittest
from unittest.mock import patch, Mock
from modules import weather
import sys
sys.path.append("..")

class TestHandleWeather(unittest.TestCase):

    @patch('modules.weather.requests.get')
    def test_handle_weather(self, mock_get):
        # Mock the response from the OpenWeather API
        mock_response = Mock()
        expected_result = {'weather': [{'description': 'clear sky'}], 'main': {'temp': 293.15}}
        mock_response.json.return_value = expected_result
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        result = weather.handle_weather("Paris")
        self.assertEqual(result, "The weather in Paris is clear sky with a temperature of 20.0°C.")

if __name__ == '__main__':
    unittest.main()
