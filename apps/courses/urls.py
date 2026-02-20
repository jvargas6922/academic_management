from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='course_list'),
    path('create/', views.create_course, name='create_course'),
    path('edit/<int:course_id>/', views.edit, name='edit_course'),
    path('update/<int:course_id>/', views.update, name='update_course'),
    path('delete/<int:course_id>/', views.delete, name='delete_course'),
]