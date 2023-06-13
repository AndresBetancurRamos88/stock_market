import requests
from django.contrib.auth import get_user_model
from drf_spectacular.utils import (OpenApiExample, OpenApiParameter,
                                   extend_schema)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.viewsets import GenericViewSet

from .models import MarketLog
from .serializers import MarketSerializer
from .throttle import PerMinuteThrottle


class MarketViewsets(GenericViewSet):
    throttle_classes = [AnonRateThrottle, PerMinuteThrottle]
    serializer_class = MarketSerializer
    lookup_field = "symbol"

    def get_queryset(self, *args, **kwargs):
        symbol = kwargs.get("symbol")
        if symbol:
            return self.get_stock_market(symbol)
        return {"Error Message": "Missing symbol"}

    def get_stock_market(self, symbol: str):
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize=compact&apikey=X86NOH6II01P7R24"
        response = requests.get(url)
        data = response.json()
        if data.get("Error Message"):
            return data
        timeseries = data["Time Series (Daily)"]
        sorted_dates = sorted(timeseries.keys(), reverse=True)
        today_info = timeseries[sorted_dates[0]]
        yesterday_info = timeseries[sorted_dates[1]]
        open_price = float(today_info["1. open"])
        high_price = float(today_info["2. high"])
        low_price = float(today_info["3. low"])
        prev_close = float(yesterday_info["4. close"])
        curr_close = float(today_info["4. close"])
        variation = round(curr_close - prev_close, 1)

        return {
            "symbol": symbol,
            "open_price": open_price,
            "high_price": high_price,
            "low_price": low_price,
            "variation": variation,
        }

    def validate_user(self, key: str):
        User = get_user_model()
        try:
            return User.objects.get(key=key)
        except User.DoesNotExist:
            return {"Error Message": "User does not exist"}

    @extend_schema(
        tags=["Market"],
        parameters=[
            OpenApiParameter(
                name="symbol",
                location=OpenApiParameter.PATH,
                examples=[
                    OpenApiExample(
                        name="Stock market query",
                        value="META"
                    )
                ],
            ),
            OpenApiParameter(
                name="key",
                type={
                    "type": "object",
                    "properties": {"key": {"type": "string"}},
                    "required": ["key"],
                },
                location=OpenApiParameter.HEADER,
                examples=[
                    OpenApiExample(
                        name="Key headers",
                        value=["5bdec2b59c19962afe904f3fae20ae"]
                    )
                ],
            ),
        ],
        responses={
            200: serializer_class,
            400: {
                "type": "object",
                "properties": {
                    "Error Message": {
                        "type": "string",
                        "description": "Bad Request"
                    }
                },
            },
        },
        summary="Stock market",
        description="Stock market query by symbol and \
                returns the opening price, the highest,\
                the lowest and the closing variation \
                with respect to the previous date",
    )
    def retrieve(self, request, *args, **kwargs):
        auth_header = request.META.get("HTTP_KEY")
        user = self.validate_user(auth_header)

        if isinstance(user, dict):
            return Response(user, status=status.HTTP_400_BAD_REQUEST)

        if user:
            query_set = self.get_queryset(**kwargs)
            if query_set.get("Error Message"):
                return Response(query_set, status=status.HTTP_400_BAD_REQUEST)

            MarketLog.objects.create(**query_set, user=user)
            return Response(query_set, status=status.HTTP_200_OK)
