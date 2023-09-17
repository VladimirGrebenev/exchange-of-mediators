from django.views.generic import ListView
from user import models as mediator_model


class MediatorsListView(ListView):
    model = mediator_model.User
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objects'] = mediator_model.User.objects.all()
        return context
