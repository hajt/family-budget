from django.db.models import Q

from rest_framework.mixins import (
    DestroyModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .models import Transaction
from .serializers import TransactionSerializer


class TransactionViewSet(
    RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet
):
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get", "patch", "delete"]

    def get_queryset(self):
        queryset = Transaction.objects.filter(
            wallet__owner=self.request.user.id
        ).select_related("wallet__owner")
        if self.action == "retrieve":
            queryset = (
                Transaction.objects.filter(
                    Q(wallet__owner=self.request.user.id)
                    | Q(wallet__participants__in=[self.request.user.id])
                )
                .select_related("wallet__owner")
                .prefetch_related("wallet__participants")
            )
        return queryset
