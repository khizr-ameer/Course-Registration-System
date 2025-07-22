# registration/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('student/', views.student_panel, name='student_panel'),
    path('admiin/', views.admin_panel, name='admin_panel'),
    path('create_course/', views.create_course, name='create_course'),
    path('delete_course/', views.delete_course, name='delete_course'),
    path('display_all_courses/', views.display_all_courses, name='display_all_courses'),
    path('add_student/', views.add_student, name='add_student'),
    path('delete_student/', views.delete_student, name='delete_student'),
    path('display_all_students/', views.display_all_students, name='display_all_students'),
    path('enroll_student/', views.enroll_student, name='enroll_student'),
    path('drop_registration/', views.drop_registration, name='drop_registration'),
    path('display_enrolled_students/', views.display_enrolled_students, name='display_enrolled_students'),
    path('display_enrolled_courses/', views.display_enrolled_courses, name='display_enrolled_courses'),
]
