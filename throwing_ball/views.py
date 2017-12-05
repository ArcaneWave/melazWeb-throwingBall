from django.shortcuts import render

from .forms import ThrowingBallForm
from .app import system


# Create your views here.
def index(request):
    return render(request, 'common/index.html', {})


def throw_ball(request):
    if request.method == 'POST':
        form = ThrowingBallForm(request.POST)

        if form.is_valid():
            pass

        powers = []
        if form.cleaned_data['using_complex_gravity']:
            powers.append('Сила тяжести с зависимостью от высоты: \( g = g(y) \)')
        if form.cleaned_data['using_archimedes_force']:
            powers.append(
                'Сила Архимеда: \( \\rho_{{тела}} = {body_density}\ кг/м^3, \\rho_{{среды}} = {environment_density}\ '
                'кг/м^3 \)'.
                format(body_density=form.cleaned_data['body_density'],
                       environment_density='вычисляется\ по\ таблице' if
                       form.cleaned_data['water_environment'] else form.cleaned_data['environment_density']))
        if form.cleaned_data['using_environment_resistance']:
            powers.append(
                'Коэффициент сопротивления окружающей среды: \( k_{{сопротивления}} = {resistance_coefficient} \)'.
                format(resistance_coefficient=form.cleaned_data['resistance_coefficient']))
        if form.cleaned_data['using_wind']:
            powers.append('Скорость ветра/течения: \( v_{{ветра/течения}} = {wind_speed}\ м/с \)'.
                          format(wind_speed=form.cleaned_data['wind_speed']))

        response = render(request, 'main/experiment.html', {
            'title': 'Моделирование движения тела, брошенного под углом к горизонту',
            'form': form,
            'powers': powers
        })
        response.set_cookie(key='using_complex_gravity', value=form.cleaned_data['using_complex_gravity'])
        response.set_cookie(key='using_archimedes_force', value=form.cleaned_data['using_archimedes_force'])
        response.set_cookie(key='using_environment_resistance', value=form.cleaned_data['using_environment_resistance'])
        response.set_cookie(key='using_wind', value=form.cleaned_data['using_wind'])
        response.set_cookie(key='water_environment', value=form.cleaned_data['water_environment'])

    else:
        form = ThrowingBallForm()

        response = render(request, 'main/experiment.html', {
            'title': 'Моделирование движения тела, брошенного под углом к горизонту',
            'form': form
        })
        response.set_cookie(key='using_complex_gravity', value=False)
        response.set_cookie(key='using_archimedes_force', value=False)
        response.set_cookie(key='using_environment_resistance', value=False)
        response.set_cookie(key='using_wind', value=False)
        response.set_cookie(key='water_environment', value=False)

    return response
