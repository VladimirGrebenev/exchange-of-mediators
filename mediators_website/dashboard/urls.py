from django.urls import path
from django.views.generic import TemplateView

import dashboard.views as views

from user.views import DashboardProfileView

app_name = "dashboard"

urlpatterns = [
    path("", views.DashboardDispatcherView.as_view(), name='dashboard'),
    path("user/", views.UserDashboardView.as_view(template_name = 'dashboard/page-dashboard.html'), name='user_dashboard'),
    path("mediator/", views.MediatorsDashboardView.as_view(template_name = 'dashboard/page-dashboard.html'), name='mediator_dashboard'),
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
        'user/manage-jobs/',
        views.UserDashboardListConflictsView.as_view(
            template_name='dashboard/page-dashboard-manage-jobs.html'),
        name='jobs'
    ),
    path(
        'mediator/manage-jobs-mediator/',
        views.MediatorDashboardListConflictsView.as_view(
            template_name='dashboard/page-dashboard-manage-jobs-mediator.html'),
        name='jobs-mediator'
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
        DashboardProfileView.as_view(
            template_name='dashboard/page-dashboard-profile.html'),
        name='profile'),
]
