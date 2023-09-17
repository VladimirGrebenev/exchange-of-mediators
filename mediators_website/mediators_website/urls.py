from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.urls import include, path
from mediators_website import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path(
        'mediators/',
        views.MediatorsListView.as_view(
            template_name='page-about.html'),
        name='mediators'),
    # path(
    #     'mediators/',
    #     TemplateView.as_view(
    #         template_name='page-about.html'),
    #     name='mediators'),
    path(
        'contacts/',
        TemplateView.as_view(
            template_name='page-contact.html'),
        name='contacts'),
    path(
        'error/',
        TemplateView.as_view(
            template_name='page-error.html'),
        name='error'),
    path(
        'faq/',
        TemplateView.as_view(
            template_name='page-faq.html'),
        name='faq'),
    path(
        'terms/',
        TemplateView.as_view(
            template_name='page-terms.html'),
        name='terms'),
    path(
        'mediators/',
        TemplateView.as_view(
            template_name='page-about.html'),
        name='mediators'
    ),
    path("user/", include("user.urls", namespace="user")),
    path("signing/", include("signing.urls", namespace="signing")),
    path("conflict/", include("conflict.urls", namespace="conflict")),
    path("dashboard/", include("dashboard.urls", namespace="dashboard")),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
