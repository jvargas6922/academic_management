from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='teacher_list'),
    path('create/', views.create, name='create_teacher'),
    path('edit/<int:teacher_id>/', views.edit, name='edit_teacher'),
    path('update/<int:teacher_id>/', views.update, name='update_teacher'),
    path('delete/<int:teacher_id>/', views.delete, name='delete_teacher'),
]