from django.contrib import admin

from .models import MarketLog


class MarketAdmin(admin.ModelAdmin):
    list_display = (
        "symbol",
        "open_price",
        "high_price",
        "low_price",
        "variation",
        "user",
    )
    list_filter = ("user",)


admin.site.register(MarketLog, MarketAdmin)
