from django.db import models
from django.utils import timezone

from apps.users.models import User


class MarketLog(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateTimeField(
        verbose_name="Creation date", default=timezone.now
    )
    symbol = models.CharField(verbose_name="Market", max_length=20)
    open_price = models.FloatField(verbose_name="open_price")
    high_price = models.FloatField(verbose_name="high_price")
    low_price = models.FloatField(verbose_name="low_price")
    variation = models.FloatField(verbose_name="variation")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="User"
    )
