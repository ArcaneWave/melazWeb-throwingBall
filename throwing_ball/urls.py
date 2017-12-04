from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('throw_ball', views.throw_ball, name='throw_ball'),
]
