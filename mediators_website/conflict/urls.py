from django.urls import path
from .views import ConflictView

app_name = 'conflict'

urlpatterns = [
    path('', ConflictView.as_view()),
]
