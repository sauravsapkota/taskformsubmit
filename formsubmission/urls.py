from django.urls import path
from .views import UserListView, UserCreateView, UserDetailView, UserUpdateView, UserDeleteView, UserUndeleteView

urlpatterns = [
    path('', UserCreateView.as_view(), name='register_user'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('user_detail/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('user_update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('user/delete/<int:pk>/', UserDeleteView.as_view(), name="user_delete"),
    path('user/undelete/<int:pk>/', UserUndeleteView.as_view(), name="user_undelete"),
]