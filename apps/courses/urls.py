from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='course_list'),
    path('create/', views.create_course, name='create_course'),
]