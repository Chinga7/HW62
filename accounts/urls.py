from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.views import RegisterView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    # path('list/', UserListView.as_view(), name='list'),
    # path('<int:pk>/', UserDetailView.as_view(), name='detail'),
    # path('change/', UserChangeView.as_view(), name='change'),
    # path('password_change/', UserPasswordChangeView.as_view(), name='password_change')
]