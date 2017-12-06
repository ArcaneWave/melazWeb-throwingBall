from django import forms

from .models import ThrowingBall


class ThrowingBallForm(forms.ModelForm):
    class Meta:
        model = ThrowingBall
        exclude = ()

    graphic_to_display = forms.CharField(label='График', max_length=2, widget=forms.RadioSelect(
        attrs={}, choices=(
            ('x', 'Зависимости координаты x от времени'),
            ('y', 'Зависимости координаты y от времени'),
            ('vx', 'Зависимости компоненты x скорости от времени'),
            ('vy', 'Зависимости компоненты y скорости от времени')
        )))
