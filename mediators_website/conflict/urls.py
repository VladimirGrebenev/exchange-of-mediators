from django.urls import path
from conflict.views import ConflictView, DocumentFormView, ConflictFormView, ConflictCreateView

app_name = 'conflict'

urlpatterns = [
    # temporary views
    path('', ConflictView.as_view(), name='conflict'),

    # conflicts
    path('create/', ConflictCreateView.as_view(), name='create_conflict'),

    # forms
    path('get-conflict-form/', ConflictFormView.as_view(), name='conflict_form'),
    path('get-document-form/', DocumentFormView.as_view(), name='document_form'),
]
