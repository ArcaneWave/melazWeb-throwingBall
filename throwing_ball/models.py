from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.
class ThrowingBall(models.Model):
    body_mass = models.FloatField('Масса тела, кг', default=1, validators=[
        MinValueValidator(0)
    ])
    start_x = models.FloatField('Начальная координата по оси X, м', default=0)
    start_y = models.FloatField('Начальная координата по оси Y, м', default=100)
    start_speed = models.FloatField('Скорость тела в начальный момент времени, м/с', default=10)
    start_angle = models.FloatField('Угол, под которым брошено тело, °C', default=45)
    experiment_time = models.IntegerField('Длительность эксперимента, сек', default=10)
    step_amount = models.IntegerField('Число временных отсчётов', default=100)
    using_complex_gravity = models.BooleanField('Сила тяжести с зависимостью от высоты', default=False)
    using_archimedes_force = models.BooleanField('Сила Архимеда', default=False)
    using_environment_resistance = models.BooleanField('Сила сопротивления среды', default=False)
    using_wind = models.BooleanField('Ветер', default=False)
    body_density = models.IntegerField('Плотность тела, кг/м^3', default=4200)
    environment_density = models.IntegerField('Плотность окружающей среды', default=1000)
    resistance_coefficient = models.FloatField('Коэффициент сопротивления окружающей среды', default=1)
    wind_speed = models.FloatField('Скорость ветра, м/с', default=-4)
    water_environment = models.BooleanField('Водная среда', default=False)
