from rest_framework.routers import DefaultRouter

from .views import MarketViewsets

router = DefaultRouter()
router.register(r"market", MarketViewsets, basename="market")
urlpatterns = router.urls
