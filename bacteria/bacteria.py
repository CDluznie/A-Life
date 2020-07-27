import random, math

class Bacteria:

    PROBABILITY_STRAIGHT_INCREASE = 0.9
    PROBABILITY_STRAIGHT_DECREASE = 0.5

    def __init__(self, x, y, vx, vy, velocity, density):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.velocity = velocity
        self.density = density
        
    @staticmethod
    def random(environment, velocity):
        x = random.random()*environment.L
        y = random.random()*environment.L
        vx, vy = Bacteria.__random_direction(velocity)
        old_density = environment.density(x,y)
        return Bacteria(x, y, vx, vy, velocity, old_density) 

    @staticmethod
    def __random_direction(velocity):
        alpha = random.random()*math.pi*2
        vx = math.cos(alpha) * velocity
        vy = math.sin(alpha) * velocity
        return vx, vy
        
    def __is_going_forward(self, current_density):
        if current_density > self.density:
            if random.random() < Bacteria.PROBABILITY_STRAIGHT_INCREASE:
                return True
        if random.random() < Bacteria.PROBABILITY_STRAIGHT_DECREASE:
            return True
        return False

    def update(self, environment, dt):
        current_density = environment.density(self.x, self.y)
        if not self.__is_going_forward(current_density):
            self.vx, self.vy = Bacteria.__random_direction(self.velocity)
        self.x += self.vx * dt
        self.y += self.vy * dt
        # TODO remove periodicity and add wall management
        self.x %= environment.L
        self.y %= environment.L
        self.density = current_density
