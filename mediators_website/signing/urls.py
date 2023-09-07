from django.urls import path

from signing.views import SignInView

app_name = 'signing'
urlpatterns = [
    path('register/', SignInView.as_view(), name='register')
]
