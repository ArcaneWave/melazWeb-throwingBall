from math import cos, sin, sqrt, pi

density_table = {120000: 0.000000002440, 100000: 0.0000000555, 50000: 0.0001027, 20000: 0.089,
                 15000: 0.195, 12000: 0.312, 10000: 0.414, 8000: 0.526, 5000: 0.736, 3000: 0.909, 2000: 1.007,
                 1000: 1.112, 500: 1.167, 300: 1.190, 200: 1.202, 100: 1.213, 50: 1.219, 0: 1.225}


class System:
    def __init__(self,
                 body_mass=0, start_x=0, start_y=100, start_speed=10, start_angle=45, experiment_time=10,
                 step_amount=100,  # Main
                 using_complex_gravity=False,  # Gravity
                 using_archimedes_force=False, body_density=None, environment_density=None,  # Archimedes force
                 using_environment_resistance=False, resistance_coefficient=None,  # Linear velocity dependence
                 using_wind=False, wind_speed=None,  # Wind
                 ):

        # Main
        start_angle = abs(start_angle - 90) % 180 / 180 * pi
        self.currentTime = 0
        self.bodyMass = body_mass
        self.currentX = start_x
        self.currentY = start_y
        self.currentSpeedX = start_speed * cos(start_angle)
        self.startx = self.currentSpeedX
        self.currentSpeedY = start_speed * sin(start_angle)
        self.experimentTime = experiment_time
        self.stepAmount = step_amount
        self.result = [[0] * self.stepAmount for _ in range(11)]
        self.step = self.experimentTime / self.stepAmount

        # Gravity
        self.usingComplexGravity = using_complex_gravity

        # Archimedes force
        self.usingArchimedesForce = using_archimedes_force
        self.startEnvironmentDensity = environment_density
        self.bodyDensity = body_density

        # Environment resistance
        self.usingEnvironmentResistance = using_environment_resistance
        self.resistanceCoefficient = resistance_coefficient
        self.linearResistanceCoefficient = self.get_resistance_coefficient()  # Calculate using gotten data

        # Wind
        self.usingWind = using_wind
        self.windSpeed = wind_speed

        # Other
        self.environmentDensity = None
        self.archimedesCoefficient = None

    def perform_experiment(self):

        self.result[0][0] = self.currentTime
        self.result[1][0] = self.currentX
        self.result[2][0] = self.currentY
        self.result[3][0] = self.currentSpeedX
        self.result[4][0] = self.currentSpeedY
        self.result[5][0] = self.result[6][0] = self.result[7][0] = self.result[8][0] = self.result[9][0] = \
            self.result[10][0] = 0

        for i in range(1, self.stepAmount):
            self.environmentDensity = self.get_environment_density()
            self.archimedesCoefficient = self.get_archimedes_coefficient()

            gravity = self.get_current_gravity()
            arch_force = self.get_archimedes_force()
            resistance_x = self.get_environment_resistance_force(self.currentSpeedX)
            resistance_y = self.get_environment_resistance_force(self.currentSpeedY)
            wind_speed = self.get_wind()
            if self.currentSpeedX > 0:
                resistance_x *= -1
            if self.currentSpeedY > 0:
                resistance_y *= -1
            current_resultant_x = wind_speed + resistance_x

            current_resultant_y = -gravity + arch_force + resistance_y

            if self.currentSpeedX * current_resultant_x > 0:
                if abs(self.currentSpeedX) > abs(self.get_maximum_x_speed()):
                    if self.currentSpeedX > 0:
                        self.currentSpeedX = self.get_maximum_x_speed()
                    else:
                        self.currentSpeedX = -self.get_maximum_x_speed()
            else:
                self.currentSpeedX = self.currentSpeedX + current_resultant_x * self.step

            self.currentSpeedY = self.currentSpeedY + current_resultant_y * self.step

            if abs(self.currentSpeedY) > abs(self.get_maximum_speed()):
                if self.currentSpeedY > 0:
                    self.currentSpeedY = self.get_maximum_speed()
                else:
                    self.currentSpeedY = -self.get_maximum_speed()

            self.currentX = self.currentX + self.currentSpeedX * self.step
            self.currentY = self.currentY + self.currentSpeedY * self.step

            if self.currentY <= 0:
                if (i < 1):
                    pass
                else:
                    self.currentY = 0
                    self.currentSpeedX = 0
                    self.currentSpeedY = 0
                    gravity = arch_force = resistance_x = resistance_y = wind_speed = 0

            self.currentTime += self.step

            self.result[0][i] = self.currentTime
            self.result[1][i] = self.currentX
            self.result[2][i] = self.currentY
            self.result[3][i] = self.currentSpeedX
            self.result[4][i] = self.currentSpeedY
            self.result[5][i] = gravity
            self.result[6][i] = arch_force
            self.result[7][i] = resistance_x
            self.result[8][i] = resistance_y
            self.result[9][i] = wind_speed
            self.result[10][i] = self.environmentDensity

            if self.currentY == 0:
                for j in range(11):
                    self.result[j] = self.result[j][:i + 1:]
                break

        return self.result

    def get_environment_density(self):
        if self.usingArchimedesForce is None and self.usingEnvironmentResistance is None:
            return 0
        if self.startEnvironmentDensity and self.startEnvironmentDensity > 0:
            return self.startEnvironmentDensity
        else:
            for i in density_table.keys():
                if self.currentY > i:
                    return density_table[i]

    # Gravity
    def get_current_gravity(self):
        if self.usingComplexGravity:
            return 0.000000000067408 * (5972400000000000000000000 * self.bodyMass) / (
                    (6371000 + self.currentY) * (6371000 + self.currentY))
        else:
            return 9.81

    # Archimedes force
    def get_archimedes_coefficient(self):
        if not self.usingArchimedesForce:
            return None
        return self.environmentDensity / self.bodyDensity

    def get_archimedes_force(self):
        if self.usingArchimedesForce:
            return self.archimedesCoefficient * self.get_current_gravity()
        else:
            return 0

    # Linear velocity dependence
    def get_resistance_coefficient(self):
        if not self.usingEnvironmentResistance:
            return None
        else:
            return self.resistanceCoefficient / self.bodyMass

    def get_environment_resistance_force(self, velocity):
        if self.usingEnvironmentResistance:
            if self.environmentDensity > 2:
                return self.resistanceCoefficient * velocity
            else:
                return self.resistanceCoefficient * abs(velocity) * velocity
        else:
            return 0

    # Wind
    def get_wind(self):
        if self.usingWind:
            return self.windSpeed
        else:
            return 0

    # Main

    def get_maximum_x_speed(self):
        return abs(self.startx) + abs(self.windSpeed)

    def get_maximum_speed(self):
        if self.usingEnvironmentResistance:
            if self.environmentDensity > 2:
                return self.bodyMass * self.get_current_gravity() / self.resistanceCoefficient
            else:
                return sqrt(self.bodyMass * self.get_current_gravity() / self.resistanceCoefficient)
        else:
            return 9999999999999
