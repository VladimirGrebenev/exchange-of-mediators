from django.urls import path

from signing.views import SignupView, SigninView, SignoutView

app_name = 'signing'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='register'),
    path('signin/', SigninView.as_view(), name='login'),
    path('signout/', SignoutView.as_view(), name='logout'),
]
