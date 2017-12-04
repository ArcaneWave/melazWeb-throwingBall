from django.shortcuts import render

from .forms import ThrowingBallForm


# Create your views here.
def index(request):
    return render(request, 'common/index.html', {})


def throw_ball(request):
    if request.method == 'POST':
        form = ThrowingBallForm(request.POST)

        response = render(request, 'main/experiment.html', {
            'title': 'Моделирование движения тела, брошенного под углом к горизонту',
            'form': form
        })
        response.set_cookie(key='using_complex_gravity', value=form.cleaned_data['using_complex_gravity'])
        response.set_cookie(key='using_archimedes_force', value=form.cleaned_data['using_archimedes_force'])
        response.set_cookie(key='using_environment_resistance', value=form.cleaned_data['using_environment_resistance'])
        response.set_cookie(key='using_wind', value=form.cleaned_data['using_wind'])
    else:
        form = ThrowingBallForm()

        response = render(request, 'main/experiment.html', {
            'title': 'Моделирование движения тела, брошенного под углом к горизонту',
            'form': form
        })

    return response
