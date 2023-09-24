from django.urls import path
from .views import CreateReview, ListReview


app_name = 'reviews'

urlpatterns = [
    path('', ListReview.as_view(), name='list_review'),
    path('create/', CreateReview.as_view(), name='create_review'),
    # path('<str:user_id>/', ListReview.as_view(), name='list_review'),
]

