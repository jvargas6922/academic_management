from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='enrollment_list'),
    path('create/', views.create_enrollment, name='create_enrollment'),
]