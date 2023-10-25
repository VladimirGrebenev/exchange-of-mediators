from django import forms
from .models import Review
from user.models import User


class ReviewForm(forms.ModelForm):
    
    class Meta:
        model = Review
        fields = ('to_user', 'from_user', 'rating', 'text')
        widgets = {
            'to_user': forms.HiddenInput,
            'from_user': forms.HiddenInput,
            'rating': forms.HiddenInput,
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'style': 'height: 100%',
                'placeholder': 'Ваш отзыв...'
            })
        }
