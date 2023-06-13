from unittest.mock import patch

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_market(client, get_key, api_data_response, mock_requests_get):
    symbol = "META"
    with patch("apps.market.views.requests.get", mock_requests_get):
        response = client.get(
            reverse("market-detail", kwargs={"symbol": symbol}),
            HTTP_KEY=get_key,
            content_type="application/json",
        )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == api_data_response
    assert "symbol" in response.json()
    assert "open_price" in response.json()


@pytest.mark.django_db
def test_market_invalid_key(client, mock_requests_get):
    symbol = "META"
    with patch("apps.market.views.requests.get", mock_requests_get):
        response = client.get(
            reverse("market-detail", kwargs={"symbol": symbol}),
            HTTP_KEY="123456",
            content_type="application/json",
        )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"Error Message": "User does not exist"}


@pytest.mark.django_db
def test_market_wrong_symbol(client, get_key, mock_requests_get):
    symbol = "QWWQEEWR"
    mesagge_wrong_symbol = {
        "Error Message": "Invalid API call. Please retry or visit the documentation (https://www.alphavantage.co/documentation/) for TIME_SERIES_DAILY_ADJUSTED."
    }
    mock_requests_get.return_value.json.return_value = mesagge_wrong_symbol
    with patch("apps.market.views.requests.get", mock_requests_get):
        response = client.get(
            reverse("market-detail", kwargs={"symbol": symbol}),
            HTTP_KEY=get_key,
            content_type="application/json",
        )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == mesagge_wrong_symbol


@pytest.mark.django_db
def test_market_throttle_success(client, get_key, mock_requests_get):
    symbol = "META"
    for _ in range(2):
        with patch("apps.market.views.requests.get", mock_requests_get):
            response = client.get(
                reverse("market-detail", kwargs={"symbol": symbol}),
                HTTP_KEY=get_key,
                content_type="application/json",
            )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_market_throttle_fail(client, get_key, mock_requests_get):
    symbol = "META"
    for _ in range(5):
        with patch("apps.market.views.requests.get", mock_requests_get):
            response = client.get(
                reverse("market-detail", kwargs={"symbol": symbol}),
                HTTP_KEY=get_key,
                content_type="application/json",
            )
    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
    assert response.json() == {
        "detail": "Request was throttled. Expected available in 60 seconds."
    }
