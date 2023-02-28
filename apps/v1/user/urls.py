from django.urls import path
from apps.v1.user import views

urlpatterns = [
    path('register/', views.register, name='user_register'),
    path('register/reset/', views.reset, name='register_reset'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
]
