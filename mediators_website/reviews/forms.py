from django import forms
from .models import Review
from user.models import User


class ReviewForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['from_user'].initial = self.initial.get('from_user')

    class Meta:
        model = Review
        fields = ('to_user', 'from_user', 'rating', 'text')
        widgets = {
            'to_user': forms.Select(attrs={'class': 'form-control'}),
            'from_user': forms.HiddenInput,
            'rating': forms.HiddenInput,
            'text': forms.Textarea(attrs={'class': 'form-control', 'row': 5})
        }
