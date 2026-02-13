from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='list_students'),
    path('create/', views.create, name='create_student'),
]