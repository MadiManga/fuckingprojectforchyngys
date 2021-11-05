from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import RegistrationView,LoginView,AccountView




urlpatterns = [
    path('',views.MainPage),
    path('login',LoginView.as_view(),name='login'),
    path('registration',RegistrationView.as_view(),name='registration'),
    path('account',AccountView.as_view(),name="account"),
    path('about-us',views.AboutUs),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
