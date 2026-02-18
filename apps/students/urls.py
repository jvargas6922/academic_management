from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='list_students'),
    path('create/', views.create, name='create_student'),
    path('edit/<int:student_id>/', views.edit, name='edit_student'),
    path('update/<int:student_id>/', views.update, name='update_student'),
    path('delete/<int:student_id>/', views.delete, name='delete_student'),
]