from django.urls import path 
from . import views
urlpatterns=[
    path('loginhome/',views.loginhome,name='loginhome'),
    path('login_process/',views.login_process,name='login_process'),
    path('registration/', views.registration, name='registration'),
    path('userreg_process/', views.userreg_process, name='userreg_process'),
    path('logout/', views.logout_view, name='logout'),
]