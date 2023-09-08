# from django.shortcuts import render
#
#
# def appeal(request):
#     return render(request, 'appeal.html')

from django.views.generic import TemplateView
from .forms import ConflictForm, ConflictFileForm
from django.views.decorators import csrf
from django.views.decorators.csrf import csrf_protect


class ConflictView(TemplateView):
    """ form of appeal """
    template_name = "conflict.html"

    def get_context_data(self, **kwargs):
        context = super(ConflictView, self).get_context_data(**kwargs)
        conflict_form = ConflictForm()
        document_form = ConflictFileForm()
        context['text'] = conflict_form
        context['document'] = document_form

        return context
