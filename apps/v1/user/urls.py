from django.urls import path
from apps.v1.user import views

urlpatterns = [
    path('register/', views.register, name='user_register'),
    path('login/', views.login, name='user_login'),
]
