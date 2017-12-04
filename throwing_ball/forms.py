from django import forms

from .models import ThrowingBall


class ThrowingBallForm(forms.ModelForm):
    class Meta:
        model = ThrowingBall
        exclude = ()
