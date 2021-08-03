from django.urls import path

from . import views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('',views.dashboard,name='dashboard'), #if someone just writes 'accounts', dashboard should be shown
    path('forgotPassword/',views.forgotPassword,name='forgotPassword'),
    path('activate/<uidb64>/<token>',views.activate,name='activate'), #activation query (account_verification_email)
    path('resetpassword_validate/<uidb64>/<token>',views.resetpassword_validate,name='resetpassword_validate'), #resetpassword_validate query (resetpassword_validate)
    path('resetPassword/',views.resetPassword,name='resetPassword'),
]
