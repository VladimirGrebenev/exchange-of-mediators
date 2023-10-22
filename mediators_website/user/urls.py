from django.urls import path

from user.views import EmailConfirmView, MediatorDetailView


app_name = 'user'
urlpatterns = [
    path(
        "email_confirm/<str:code>/",
        EmailConfirmView.as_view(),
        name="email_confirm",
    ),
]
