from django.urls import path
import dashboard.views as views

app_name = "dashboard"

urlpatterns = [
    path("", views.DashboardDispatcherView.as_view(), name='dashboard'),
    path("user/", views.UserDashboardView.as_view(), name='user_dashboard'),
    path("mediator/", views.MediatorsDashboardView.as_view(), name='mediator_dashboard')
]
