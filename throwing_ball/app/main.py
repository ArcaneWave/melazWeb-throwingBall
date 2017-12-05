import system

from tabulate import tabulate


def main():
    a = system.System(body_mass=1, start_x = 0, start_y = 100, start_speed = 15, start_angle = 45, step_amount = 100, experiment_time=100,
                        using_complex_gravity = True,
                        using_archimedes_force = True, body_density=4200, environment_density = -1,
                        using_environment_resistance = True, resistance_coefficient = 0.4,
                        using_wind = True, wind_speed = -4
                        )
    s = a.perform_experiment()
    print(s)
    # s = list(zip(*s))
    # print(tabulate(s, headers=['Time', 'X', 'Y', 'Speed X', 'Speed Y', 'Gravity', 'Archimedes', 'Resistance X', 'Resistance Y', 'Wind speed', 'Density']))


main()
