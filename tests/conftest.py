import secrets
from unittest.mock import MagicMock

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user_signup():
    return {
        "name": "Andres",
        "last_name": "Ramos",
        "email": "test_user@test.com",
    }


@pytest.fixture
def api_data():
    return {
        "Meta Data": {
            "1. Information": "Daily Time Series with Splits and Dividend Events",
            "2. Symbol": "META",
            "3. Last Refreshed": "2023-06-09",
            "4. Output Size": "Compact",
            "5. Time Zone": "US/Eastern",
        },
        "Time Series (Daily)": {
            "2023-06-09": {
                "1. open": "262.48",
                "2. high": "267.949",
                "3. low": "261.7",
                "4. close": "264.95",
                "5. adjusted close": "264.95",
                "6. volume": "16949794",
                "7. dividend amount": "0.0000",
                "8. split coefficient": "1.0",
            },
            "2023-06-08": {
                "1. open": "260.62",
                "2. high": "267.65",
                "3. low": "258.88",
                "4. close": "264.58",
                "5. adjusted close": "264.58",
                "6. volume": "20899359",
                "7. dividend amount": "0.0000",
                "8. split coefficient": "1.0",
            },
        },
    }


@pytest.fixture
def api_data_response():
    return {
        "symbol": "META",
        "open_price": 262.48,
        "high_price": 267.949,
        "low_price": 261.7,
        "variation": 0.4,
    }


@pytest.fixture
def get_key(user_signup):
    User = get_user_model()
    user = User.objects.create(
        **user_signup,
        key=secrets.token_hex(15),
    )
    return user.key


@pytest.fixture
def mock_requests_get(api_data):
    mock_get = MagicMock(name="get")
    mock_get.return_value.status_code = status.HTTP_200_OK
    mock_get.return_value.json.return_value = api_data
    return mock_get
