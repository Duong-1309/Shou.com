from django.urls import path

from .. import views

from . import api

app_name = 'account'

urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('register/', views.register_account, name='register'),
    path('activate/<str:token>/', views.activate_account, name='activate'),
    path('logout', views.logout, name='logout'),
]

urlpatterns += api.urlpatterns
