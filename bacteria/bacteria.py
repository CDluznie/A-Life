from __future__ import print_function 
import random, math, numpy
import matplotlib.pyplot as plt


class Environment:

    def __init__(self, L):
        self.L = L
        
        self.sx = 4 * self.L / 5
        self.sy = 3 * self.L / 5
        self.s = 1
        self.sigma = 2e-5
        
    def density(self, x, y):
        """
        return 1./(1. + math.hypot(x-self.sx, y-self.sy) + self.s)
        """
        sigma = self.sigma
        if sigma <= 1e-5:
            return 0
        return self.s*numpy.exp(-((x - self.sx)**2/(2*sigma*sigma) + (y - self.sy)**2/(2*sigma*sigma)))

    def place_droplet(self, x, y):
        print(x,y)
        self.sigma = 2e-5
        self.sx = x
        self.sy = y
		

    def update(self):
        #self.s -= 0.005
        self.sigma *= 0.995

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
        #domain periodicity:
        self.x %= environment.L
        self.y %= environment.L
        self.density = current_density

    
class World:
	
    DT = 0.2
    VELOCITY = 3e-6
    L = 100e-6
	
    def __init__(self, environment, bacterias):
        self.environment = environment
        self.bacterias = bacterias
    
    @staticmethod
    def random(number_bacterias):
        environment = Environment(World.L)
        bacterias = [
            Bacteria.random(environment, World.VELOCITY)
            for _ in range(number_bacterias)
        ]
        return World(environment, bacterias)
    
    def simulate(self):
        t = 0
        while True:
            self.draw(t)
            for bacteria in self.bacterias:
                bacteria.update(self.environment, World.DT)
            self.environment.update()
            t += World.DT

    def draw(self, t):
        n = 100
        m = numpy.zeros((n,n))
        for x in range(n):
            for y in range(n):
                m[y,x] = self.environment.density(x*self.environment.L/n,y*self.environment.L/n)
        for bacteria in self.bacterias:
            x,y = int((bacteria.x*n/self.environment.L)), int((bacteria.y*n/self.environment.L))  # TODO ERROR ROUND WITH BOUND MAX OF ARRAY
            m[y,x] = 1
        figure = plt.figure(1)
        plt.clf()
        plt.axis("off")
        plt.imshow(m)
        figure.canvas.mpl_connect('button_press_event', lambda e:
			self.environment.place_droplet(e.xdata*self.environment.L/n, e.ydata*self.environment.L/n)
		)
        plt.pause(0.001)
        
    def draw2(self, t):
        n = 100
        m = numpy.zeros((n,n,3))
        
        for x in range(n):
            for y in range(n):
                m[y,x,0] = self.environment.density(x*self.environment.L/n,y*self.environment.L/n)
        
        print(m[:,:,0])
        
        plt.figure(1)
        plt.clf()
        plt.axis("off")
        plt.imshow(m)
        plt.pause(0.001)

world = World.random(100)

world.simulate()
