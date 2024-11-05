from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import RegisterView, LoginView, UserDetailView
from .views import LogoutView,Imageupload,ChangePassword,ResourceView
from .views import LogoutView,Imageupload,ChangePassword
from .views import AddWorkerView
 
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('logout/',LogoutView.as_view(), name='logout'),
    path('upload/',Imageupload.as_view(),name='upload'),
    path('change_password/',ChangePassword.as_view(),name='password_change'),

    path('resources/',ResourceView.as_view(),name='enter resources'),
    path('resources/<str:resource_type>/<int:pk>/', ResourceView.as_view(), name='resource-detail'),
    path('add_worker/', AddWorkerView.as_view(), name='add-worker'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)