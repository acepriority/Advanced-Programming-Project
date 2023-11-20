from django.urls import path
from . import views 
from .views import process_image

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'), 
    path('register/', views.register_user, name='register'),
    path('process_image/', process_image, name='process_image')
]