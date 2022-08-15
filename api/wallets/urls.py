from rest_framework import routers

from .views import WalletViewSet


wallets_router = routers.SimpleRouter()
wallets_router.register("wallets", WalletViewSet, basename="wallets")

urlpatterns = wallets_router.urls
