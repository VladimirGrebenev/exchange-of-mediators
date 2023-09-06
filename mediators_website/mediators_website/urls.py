from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path(
        'mediators/',
        TemplateView.as_view(
            template_name='page-about.html'),
        name='mediators'
    ),
    path(
        'dashboard/',
        TemplateView.as_view(
            template_name='page-dashboard.html'
        ),
        name='dashboard'
    ),
    path(
        'contacts/',
        TemplateView.as_view(
            template_name='page-contact.html'),
        name='contacts'
    ),
    path('login/',
         TemplateView.as_view(
             template_name='page-login.html'
         ),
         name='login'
         ),
    path(
        'register/',
        TemplateView.as_view(
            template_name='page-register.html'
        ),
        name='register'
    ),
    path(
        'error/',
        TemplateView.as_view(
            template_name='page-error.html'
        ),
        name='error'
    ),
    path(
        'faq/',
        TemplateView.as_view(
            template_name='page-faq.html'),
        name='faq'
    ),
    path(
        'terms/',
        TemplateView.as_view(
            template_name='page-terms.html'),
        name='terms'
    ),
    path("users/", include("user.urls", namespace="users")),
    path("signing/", include("signing.urls", namespace="signing")),
]
