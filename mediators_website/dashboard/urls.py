from django.urls import path
from django.views.generic import TemplateView

import dashboard.views as views
from conflict.views import ConflictFormView, ConflictView, ConflictCreateView

from user.views import DashboardProfileView, TopMediatorsList

app_name = "dashboard"

urlpatterns = [
    path("", views.DashboardDispatcherView.as_view(), name='dashboard'),
    path("user/", views.UserDashboardView.as_view(), name='user_dashboard'),
    path("mediator/", views.MediatorsDashboardView.as_view(), name='mediator_dashboard'),
    # path('conflict/', ConflictView.as_view(), name='conflict'),
    path(
        'create-project/',
        ConflictCreateView.as_view(
            template_name='dashboard/page-dashboard-create-project.html'),
        name='create-project'
    ),
    path('get-conflict-form/', ConflictFormView.as_view(), name='conflict_form'),
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
        'user/list-mediator/',
        TopMediatorsList.as_view(
            template_name='dashboard/page-dashboard-list-mediators.html'),
        name='list-mediators'
    ),
    path(
        'user/manage-jobs/status-new/',
        views.UserDashboardListConflictStatusNew.as_view(),
        name='new'
    ),
    path(
        'user/manage-jobs/status-in-work/',
        views.UserDashboardListConflictStatusInWork.as_view(),
        name='in-work'
    ),
    path(
        'user/manage-jobs/status-completed/',
        views.UserDashboardListConflictStatusCompleted.as_view(),
        name='completed'
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
    path(
        'mediator/new-conflicts-list/',
        TemplateView.as_view(
            template_name='dashboard/page-dashboard-new-conflicts-list.html'),
        name='new-conflicts-list'
    ),
]
