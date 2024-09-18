from django.urls import path
from . import views

app_name = 'api-v1'
urlpatterns = [
    path('registration/', views.RegistrationApiView.as_view(), name='registration'),
    path('change-password/', views.ChangePasswordApiView.as_view(), name='change-password'),
    path('profile/<int:pk>/', views.ProfileApiView.as_view(), name='profile'),
    # login with verify
    path('api-token-auth/', views.CustomAuthToken.as_view(), name='login-verify'),
    path('activication/confirm/<str:token>', views.ActivationApiView.as_view(), name='activation'),
]