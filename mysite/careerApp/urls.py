from django.contrib import admin
from django.urls import include, path

from careerApp import views

urlpatterns = [
path('quizStartApti/',views.quizStartApti,name='quizStartApti'),
path('',views.studentDashboardView,name='studDashboard'),
path('quizStartApti/',views.quizStartApti,name='quizStartApti'),
path('ajax/save-answer/', views.saveAnswer, name="save-answer"),
path('quizStartInt/',views.quizStartInt,name='quizStartInt'),
path('ajax/save-answer1/', views.saveAnswer1, name="save-answer1"),

path('quizForCareer/',views.indexCareer,name='indexCareer'),
path('login', views.loginView, name='loginUrl'),
path('logout/', views.logoutView, name='logout'),


]
