# from django.urls import path
# from . import views
# app_name = 'appeal'
#
# urlpatterns = [
# 	path('', views.appeal, name='appeal'),
# ]

from django.urls import path
from .views import ConflictView

app_name = 'conflict'

urlpatterns = [
    path('', ConflictView.as_view()),
]
