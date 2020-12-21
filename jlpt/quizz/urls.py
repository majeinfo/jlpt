from django.urls import path

from . import views

urlpatterns = [
    path('run_quizz', views.run_quizz, name='run_quizz'),
    path('check_quizz', views.check_quizz, name='check_quizz'),
    path('run_verbs', views.run_verbs, name='run_verbs'),
    path('check_verbs', views.check_verbs, name='check_verbs'),
    path('', views.index, name='index'),
]