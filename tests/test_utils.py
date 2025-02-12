from unittest.mock import patch, Mock
from src.utils import convert_currency, result_ticker
import pytest

@patch('requests.request')
def test_convert_currency(mock_get):
    """Тестирование функции запроса стоимости валют """
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 97.02}
    mock_get.return_value = mock_response

    user_settings = {"user_currencies": ["USD"]}
    result = convert_currency(user_settings)

    assert result == [{"currency_rates": "USD", "rate": 97.02}]


@patch('requests.get')
def test_result_ticker(mock_get):
    """Тестирование функции запроса на стоимость акции S&P500 """
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"values": [{"close": 227.63}]}
    mock_get.return_value = mock_response

    user_settings = {"user_stocks": ["AAPL"]}
    result = result_ticker(user_settings)

    assert result == [{"stock": "AAPL", "price": 227.63}]


@patch('requests.request')
def test_convert_currency_key_error(mock_get):
    """Тестирование функции при возникновении ошибки KeyError"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.side_effect = KeyError
    mock_get.return_value = mock_response

    user_settings = {"user_currencies": ["USD"]}
    result = convert_currency(user_settings)

    assert len(result) == 0


@patch('requests.get')
def test_result_ticker_key_error(mock_get):
    """Тестирование функции при возникновении ошибки KeyError"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.side_effect = KeyError
    mock_get.return_value = mock_response

    user_settings = {"user_stocks": ["AAPL"]}
    result = result_ticker(user_settings)

    assert len(result) == 0






