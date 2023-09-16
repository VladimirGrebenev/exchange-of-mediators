# from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from conference import models as conferences_model


class ConferencesListView(ListView):
    model = conferences_model
    # template_name = 'conference.html'  # for future
    # context_object_name = 'conference' # for future


class ConferencesCreateView(CreateView):
    model = conferences_model
    # template_name = 'conferences_create.html'  # for future
    # context_object_name = 'conferences_list' # for future


class ConferencesUpdateView(UpdateView):
    model = conferences_model
    # template_name = 'conferences_update.html'  # for future
    # context_object_name = 'conferences_list' # for future


class ConferencesDeleteView(DeleteView):
    model = conferences_model
    # template_name = 'conferences_delete.html'  # for future
    # context_object_name = 'conferences_list' # for future
