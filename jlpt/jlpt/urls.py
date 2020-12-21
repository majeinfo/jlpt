"""jlpt URL Configuration
"""
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quizz/', include('quizz.urls')),
    path('', include('quizz.urls')) #, namespace='quizz')),
]
