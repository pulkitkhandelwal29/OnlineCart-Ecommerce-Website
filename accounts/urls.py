from django.urls import path

from . import views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('',views.dashboard,name='dashboard'), #if someone just writes 'accounts', dashboard should be shown
    path('activate/<uidb64>/<token>',views.activate,name='activate'), #activation query
]
