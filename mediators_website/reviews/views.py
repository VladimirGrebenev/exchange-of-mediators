from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import  render
from django.views.generic import ListView,View
from .forms import ReviewForm
from .models import Review


class CreateReview(View):
    form_class = ReviewForm
    template_name = 'user/page-mediator-about.html'

    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/user/')
        return render(request, self.template_name, {'form': form})

    def get(self, request, **kwargs):
        form = ReviewForm(initial={'from_user': request.user.id})
        return render(request, self.template_name, {'form': form,})
    


class ListReview(ListView):
    model = Review
    template_name = 'reviews/reviews-list-reviews.html'
    context_object_name = 'reviews'
    