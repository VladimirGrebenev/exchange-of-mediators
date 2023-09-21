from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import CreateView, ListView
from .forms import ReviewForm
from .models import Review, User


class CreateReview(LoginRequiredMixin, CreateView):
    form_class = ReviewForm
    template_name = 'reviews/reviews-create-review.html'

    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/reviews')
        return render(request, 'reviews/reviews-create-review.html', {'form': form})

    def get(self, request, **kwargs):
        form = ReviewForm(initial={'from_user': request.user.id})
        # пишем отзывы на медиаторов
        # form.fields['to_user'].queryset = User.objects.filter(groups__name='mediator')
        return render(request, 'reviews/reviews-create-review.html', {'form': form})


class ListReview(ListView):
    model = Review
    template_name = 'reviews/reviews-list-reviews.html'
    context_object_name = 'reviews'
