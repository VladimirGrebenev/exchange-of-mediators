from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, CreateView
from .forms import ReviewForm
from .models import Review


class CreateReview(CreateView):
    form_class = ReviewForm
    template_name = 'user/page-mediator-about.html'

    # def post(self, request, *args, **kwargs):
    #     form = ReviewForm(request.POST)
    #
    #     if form.is_valid():
    #         self.form_valid(form)
    #     return HttpResponseRedirect(reverse('mediator-about', args=(form.cleaned_data.get('to_user').id,)))


class ListReview(ListView):
    model = Review
    template_name = 'reviews/reviews-list-reviews.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        if self.request.user.groups.first().name == 'mediator':
            return self.request.user.reviews.all()
        else:
            return self.request.user.created_reviews.all()
    