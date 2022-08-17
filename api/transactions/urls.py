from rest_framework import routers

from .views import TransactionViewSet


transactions_router = routers.SimpleRouter()
transactions_router.register(
    "transactions", TransactionViewSet, basename="transactions"
)

urlpatterns = transactions_router.urls
