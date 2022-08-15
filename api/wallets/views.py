from django.db.models import Q

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import ModelViewSet

from .models import Wallet
from .serializers import (
    WalletDetailSerializer,
    WalletSerializer,
    WalletUpdateSerializer,
)


# TODO: Add filter and pagination


class WalletViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get", "post", "patch", "delete"]
    serializer_class = WalletUpdateSerializer

    def get_queryset(self):
        if self.action == "shared":
            queryset = Wallet.objects.filter(
                participants__in=[self.request.user.id]
            ).order_by("name")
        elif self.action == "retrieve":
            queryset = Wallet.objects.filter(
                Q(owner=self.request.user.id)
                | Q(participants__in=[self.request.user.id])
            ).prefetch_related("participants")
        else:
            queryset = (
                Wallet.objects.filter(owner=self.request.user.id)
                .prefetch_related("participants")
                .order_by("name")
            )
        return queryset

    def get_serializer_class(self):
        if self.action in ["list", "shared"]:
            serializer = WalletSerializer
        elif self.action == "retrieve":
            serializer = WalletDetailSerializer
        else:
            serializer = self.serializer_class
        return serializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)

        return Response(serializer.data, status=HTTP_201_CREATED)

    @action(methods=["get"], detail=False, url_path="shared")
    def shared(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
