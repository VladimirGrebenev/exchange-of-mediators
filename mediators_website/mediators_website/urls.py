from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static

from user.views import TopMediatorsList, ContactTopMediatorsList,  MediatorAboutView, ClientAboutView, delete_avatar

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path(
        'contacts/',
        ContactTopMediatorsList.as_view(
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
        TopMediatorsList.as_view(
            template_name='page-about.html'),
        name='mediators'
    ), 

    path('delete-avatar/', delete_avatar, name='delete_avatar'),

    path(
        'mediator-about/<str:pk>',
        MediatorAboutView.as_view(),
        name='mediator-about'
    ),
    path(
        'user-about/<str:pk>',
        ClientAboutView.as_view(),
        name='user-about'
    ),

    path("user/", include("user.urls", namespace="user")),
    path("signing/", include("signing.urls", namespace="signing")),
    # path("conflict/", include("conflict.urls", namespace="conflict")),
    path("dashboard/", include("dashboard.urls", namespace="dashboard")),
    path("reviews/", include("reviews.urls", namespace="reviews")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
