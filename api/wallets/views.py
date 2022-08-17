from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema

from django.db.models import Q

from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.viewsets import ModelViewSet

from api.transactions.models import Transaction
from api.transactions.serializers import (
    TransactionGroupedSerializer,
    TransactionSerializer,
)
from .exceptions import NotOwnerError
from .models import Wallet
from .serializers import (
    WalletDetailSerializer,
    WalletSerializer,
    WalletUpdateSerializer,
)


class WalletPagination(PageNumberPagination):
    page_size = 10


class WalletViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get", "post", "patch", "delete"]
    serializer_class = WalletUpdateSerializer
    pagination_class = WalletPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["currency", "name"]

    def get_queryset(self):
        if self.action == "shared":
            queryset = Wallet.objects.filter(
                participants__in=[self.request.user.id]
            ).order_by("name")
        elif self.action in ["retrieve", "expenses", "income"]:
            queryset = (
                Wallet.objects.filter(
                    Q(owner=self.request.user.id)
                    | Q(participants__in=[self.request.user.id])
                )
                .prefetch_related("participants")
                .select_related("owner")
            )
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

    @swagger_auto_schema(
        method="post",
        request_body=TransactionSerializer(),
        responses={HTTP_201_CREATED: TransactionSerializer()},
    )
    @swagger_auto_schema(
        method="get", responses={HTTP_200_OK: TransactionGroupedSerializer()}
    )  # FIXME: Define custom schema for TransactionGroupedSerializer
    @action(methods=["get", "post"], detail=True, url_path="expenses")
    def expenses(self, request, *args, **kwargs):
        wallet = self.get_object()
        if self.request.method == "POST":
            if self.request.user == wallet.owner:
                serializer = self._create_transaction(wallet, request.data)
                return Response(serializer.data, status=HTTP_201_CREATED)
            else:
                raise NotOwnerError
        elif self.request.method == "GET":
            expenses = Transaction.objects.filter(is_expense=True, wallet=wallet)
            return Response(
                TransactionGroupedSerializer(instance=expenses).data, status=HTTP_200_OK
            )

    @swagger_auto_schema(
        method="post",
        request_body=TransactionSerializer(),
        responses={HTTP_201_CREATED: TransactionSerializer()},
    )
    @swagger_auto_schema(
        method="get", responses={HTTP_200_OK: TransactionGroupedSerializer()}
    )  # FIXME: Define custom schema for TransactionGroupedSerializer
    @action(methods=["get", "post"], detail=True, url_path="income")
    def income(self, request, *args, **kwargs):
        wallet = self.get_object()
        if self.request.method == "POST":
            if self.request.user == wallet.owner:
                serializer = self._create_transaction(
                    wallet, request.data, is_expense=False
                )
                return Response(serializer.data, status=HTTP_201_CREATED)
            else:
                raise NotOwnerError
        elif self.request.method == "GET":
            income = Transaction.objects.filter(is_expense=False, wallet=wallet)
            return Response(
                TransactionGroupedSerializer(instance=income).data, status=HTTP_200_OK
            )

    def _create_transaction(self, wallet, data, is_expense=True):
        serializer = TransactionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(wallet=wallet, is_expense=is_expense)
        return serializer
