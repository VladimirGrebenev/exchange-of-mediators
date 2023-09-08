from django import forms

from . import models as conflict_appeal_models


class ConflictForm(forms.ModelForm):
    """ form for entering a request """

    def __init__(self, *args, user=None, **kwargs):
        ret = super().__init__(*args, **kwargs)
        if user:
            self.fields["user"].initial = user.pk
        return ret

    class Meta:
        """ visible form fields """
        model = conflict_appeal_models.Conflict
        fields = ('title', 'status', 'creator', 'respondent', 'description',
                  'description_as_visible', 'concluded_contract',
                  'personal_data_processed', 'respect_confidentiality',
                  'mediator', )
        # fields = '__all__'
        widgets = {
            "user": forms.HiddenInput(),
        }


class ConflictFileForm(forms.Form):
    # не совсем понимаю, связан ли файл с юзером.
    """ file entry form """

    def __init__(self, *args, conflict=None, **kwargs):
        ret = super().__init__(*args, **kwargs)
        if conflict:
            self.fields["appeal"].initial = conflict.pk
        return ret

    class Meta:
        """ visible form fields """
        model = conflict_appeal_models.Document
        fields = ('user', 'conflict', 'type', 'file_path', 'file_as_visible', )
        widgets = {
            "appeal": forms.HiddenInput(),
        }
