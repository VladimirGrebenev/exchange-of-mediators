from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, CreateView

from conflict.forms import ConflictForm, DocumentForm
from conflict.models import Conflict, Document


class ConflictView(TemplateView):
    """
        Temporary view. Retire in the future
    """
    template_name = 'conflict/conflict.html'
    extra_context = {
        "object_list": Conflict.objects.all().prefetch_related('files')
    }


class ConflictFormView(FormView):
    """
        Returned conflict form
    """
    template_name = "conflict/conflict_form.html"
    form_class = ConflictForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if pk := self.request.GET.get('pk'):
            try:
                conflict = Conflict.objects.get(pk=pk)
                kwargs['instance'] = conflict
            except Conflict.DoesNotExist:
                pass
        return kwargs | {"user": self.request.user}


class DocumentFormView(FormView):
    """
        Returned document form
    """
    template_name = "conflict/document_form.html"
    form_class = DocumentForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if pk := self.request.GET.get('pk'):
            try:
                document = Document.objects.get(pk=pk)
                kwargs['instance'] = document
            except Document.DoesNotExist:
                pass
        return kwargs


class ConflictCreateView(CreateView):
    model = Conflict
    form_class = ConflictForm
    success_url = reverse_lazy('conflict:conflict')

    def get_form_kwargs(self):
        return super().get_form_kwargs() | {"user": self.request.user}

    def form_valid(self, form):
        # TODO вот тут должна быть обработка приходящей формы. Там внутри лежит форма конфликта + бесконечное
        #  количество файлов. Т.е. надо вытащить все файлы + их поля из self.request.POST и как-то их разобрать.
        #  мб имеет смысл обернуть все файлы в отдельный формы и разбирать их в контроллере. Надо пробовать,
        #  я не знаю заранее, как будет работать. Сейчас конфликты создаются. Файлы - нет.
        return super().form_valid(form)
