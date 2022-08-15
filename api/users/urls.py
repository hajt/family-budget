from django.urls import path

from .views import UserDetailView, UserListView


urlpatterns = [
    path("me/", UserDetailView.as_view(), name="me"),
    path("users/", UserListView.as_view(), name="users"),
]
