from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^run_quizz$', views.run_quizz, name='run_quizz'),
    url(r'^check_quizz$', views.check_quizz, name='check_quizz'),
    url(r'^$', views.index, name='index'),
]