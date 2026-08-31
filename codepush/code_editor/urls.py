from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('execute/', views.execute_code, name='execute'),
    path('push/', views.push_to_github, name='push'),
]