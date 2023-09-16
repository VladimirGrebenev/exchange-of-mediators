from django import forms

from conflict.models import Document, Conflict


class ConflictForm(forms.ModelForm):

    def __init__(self, user, **kwargs):
        super().__init__(**kwargs)
        self.initial['creator'] = user

    class Meta:
        model = Conflict
        fields = (
            "title",
            "status",
            "mediator",
            "creator",
            "description",
            "is_all_visible",
        )
        widgets = {
            "creator": forms.HiddenInput,
        }


class DocumentForm(forms.ModelForm):

    def __init__(self, user, **kwargs):
        super().__init__(**kwargs)
        self.initial['user'] = user

    class Meta:
        model = Document
        fields = (
            "file_path",
            "user",
            "is_all_visible",
        )
        widgets = {
            "user": forms.HiddenInput,
        }
