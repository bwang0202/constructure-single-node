from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^worker/', views.worker, name='worker'),
    url(r'^worker_match/', views.worker_match, name='worker match'),
    url(r'^team_match/', views.team_match, name='team match'),
]