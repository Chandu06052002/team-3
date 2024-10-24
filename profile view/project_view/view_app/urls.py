from django.urls import path
from .views import RegisterView, LoginView, UserDetailView
from .views import LogoutView
 
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('logout/',LogoutView.as_view(), name='logout'),
]