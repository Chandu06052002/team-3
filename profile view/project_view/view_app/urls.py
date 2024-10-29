from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import RegisterView, LoginView, UserDetailView
from .views import LogoutView,Imageupload
 
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('logout/',LogoutView.as_view(), name='logout'),
     path('upload/',Imageupload.as_view(),name='upload'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)