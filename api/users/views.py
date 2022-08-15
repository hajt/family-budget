from django.db.models import Q

from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import UserDetailSerializer, UserSerializer


class UserDetailView(RetrieveUpdateAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get", "patch"]

    def get_object(self):
        return self.request.user


class UserListView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.filter(Q(is_staff=False) | Q(is_superuser=False))
