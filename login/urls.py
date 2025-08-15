from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView, name= 'login'),
    path('signup/', views.SignUP, name='signup'),
    path('logout/', views.logoutView, name='logout'),
    path('forgot-password/', views.ForgotPassword, name='forgot-password'),
    path('password-reset-sent/<str:reset_id>/', views.PasswordResetSent, name='password-reset-sent'),
    path('reset-password/<str:reset_id>/', views.ResetPassword, name='reset-password'),
    path('update-user-profile/', views.update_user_profile, name='update_user_profile'),
    
]
