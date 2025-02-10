from unittest.mock import patch, Mock
from src.utils import convert_currency, result_ticker
import pytest

@patch('requests.get')
def test_convert_currency(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"conversion_rates": {"RUB": 97.02}}
    mock_get.return_value = mock_response

    user_settings = {"user_currencies": ["USD"]}
    result = convert_currency(user_settings)

    assert result == [{"currency_rates": "USD", "rate": 97.02}]


@patch('requests.get')
def test_result_ticker(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"stock_prices": {"AAPL": 227.63}}
    mock_get.return_value = mock_response

    user_settings = {"user_stocks": ["AAPL"]}
    result = result_ticker(user_settings)

    assert result == [{"stock": "AAPL", "price": 227.63}]









