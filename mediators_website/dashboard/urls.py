from django.urls import path
from django.views.generic import TemplateView

import dashboard.views as views

app_name = "dashboard"

urlpatterns = [
    path("", views.DashboardDispatcherView.as_view(), name='dashboard'),
    path("user/", views.UserDashboardView.as_view(), name='user_dashboard'),
    path("mediator/", views.MediatorsDashboardView.as_view(), name='mediator_dashboard'),
    path(
        'create-project/',
        TemplateView.as_view(
            template_name='dashboard/page-dashboard-create-project.html'),
        name='create-project'
    ),
    path(
        'invoice/',
        TemplateView.as_view(
            template_name='dashboard/page-dashboard-invoice.html'),
        name='invoice'
    ),
    path(
        'manage-jobs/',
        TemplateView.as_view(
            template_name='dashboard/page-dashboard-manage-jobs.html'),
        name='jobs'
    ),
    path(
        'message/',
        TemplateView.as_view(
            template_name='dashboard/page-dashboard-message.html'),
        name='message'
    ),
    path(
        'payouts/',
        TemplateView.as_view(
            template_name='dashboard/page-dashboard-payouts.html'),
        name='payout'
    ),
    path(
        'profile/',
        TemplateView.as_view(
            template_name='dashboard/page-dashboard-profile.html'),
        name='profile'),
]
