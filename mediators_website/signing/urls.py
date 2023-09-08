from django.urls import path

from signing.views import SignUpView, SignInUser

app_name = 'signing'
urlpatterns = [
    path('register/', SignUpView.as_view(), name='register'),
    path('login/', SignInUser.as_view(), name='login')
]
