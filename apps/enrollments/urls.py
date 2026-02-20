from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='enrollment_list'),
    path('create/', views.create_enrollment, name='create_enrollment'),
    path('edit/<int:enrollment_id>/', views.edit, name='edit_enrollment'),
    path('update/<int:enrollment_id>/', views.update, name='update_enrollment'),
    path('delete/<int:enrollment_id>/', views.delete, name='delete_enrollment'),
]