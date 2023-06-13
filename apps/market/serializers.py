from rest_framework.serializers import ModelSerializer

from .models import MarketLog


class MarketSerializer(ModelSerializer):
    class Meta:
        model = MarketLog
        fields = [
            "symbol",
            "open_price",
            "high_price",
            "low_price",
            "variation"
        ]
