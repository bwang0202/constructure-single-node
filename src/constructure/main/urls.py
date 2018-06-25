from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^worker/', views.worker, name='worker'),
    url(r'^team/', views.team, name='team'),
    url(r'^worker_logon/', views.worker_logon, name="worker logon"),
    url(r'^team_logon/', views.team_logon, name="team logon"),
    url(r'^worker_exp/', views.worker_exp, name="worker experience"),
    url(r'^worker_certificate/', views.worker_certificate, name="worker certificate"),
    url(r'^specialty/', views.specialty, name="specialty"),
    url(r'^worker_match/', views.worker_match, name='worker match'),
    url(r'^team_match/', views.team_match, name='team match'),
]