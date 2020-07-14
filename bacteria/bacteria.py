from __future__ import print_function 
import random, math, numpy
import matplotlib.pyplot as plt


class Environment:

    def __init__(self, L, droplet_size):
        self.L = L
        
        self.droplet_size = droplet_size
        self.droplet_position = None
        
    def density(self, x, y):
        if not self.droplet_position:
            return 0
        droplet_x, droplet_y = self.droplet_position
        sigma = 2*self.droplet_size*self.droplet_size
        return numpy.exp(-((x - droplet_x)**2/(sigma) + (y - droplet_y)**2/(sigma)))

    def place_droplet(self, x, y):
        self.droplet_position = (x, y)
        
    def remove_droplet(self):
        self.droplet_position = None


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
    DROPLET_SIZE = 2e-05
    OUTPUT_IMAGE_SIZE = 100
	
    def __init__(self, environment, bacterias, environment_image):
        self.environment = environment
        self.bacterias = bacterias
        self.environment_image = environment_image
        self.is_updated = False
    
    @staticmethod
    def random(number_bacterias):
        environment = Environment(World.L, World.DROPLET_SIZE)
        bacterias = [
            Bacteria.random(environment, World.VELOCITY)
            for _ in range(number_bacterias)
        ]
        environment_image = World.__environment_to_image(environment)
        return World(environment, bacterias, environment_image)
        
    @staticmethod
    def __environment_to_image(environment):
        image = numpy.zeros((World.OUTPUT_IMAGE_SIZE, World.OUTPUT_IMAGE_SIZE))
        for x in range(World.OUTPUT_IMAGE_SIZE):
            for y in range(World.OUTPUT_IMAGE_SIZE):
                image[y,x] = environment.density(
                    x*environment.L/World.OUTPUT_IMAGE_SIZE,
                    y*environment.L/World.OUTPUT_IMAGE_SIZE
                )
        return image
    
    def simulate(self):
        t = 0
        while True:
            self.draw(t)
            for bacteria in self.bacterias:
                bacteria.update(self.environment, World.DT)
            t += World.DT

    def draw(self, t):
        image = self.environment_image.copy()
        for bacteria in self.bacterias:
            x = int((bacteria.x*World.OUTPUT_IMAGE_SIZE/self.environment.L))
            y = int((bacteria.y*World.OUTPUT_IMAGE_SIZE/self.environment.L))
            image[y,x] = 1
        figure = plt.figure(1)
        plt.clf()
        plt.axis("off")
        plt.ion()
        plt.imshow(image)
        self.is_updated = False
        figure.canvas.mpl_connect('button_press_event', lambda e: self.process_click_event(e))
        plt.pause(0.01)

    def process_click_event(self, event):
        if self.is_updated:
            return
        if event.button == 1:
            self.environment.place_droplet(
                event.xdata*self.environment.L/World.OUTPUT_IMAGE_SIZE,
                event.ydata*self.environment.L/World.OUTPUT_IMAGE_SIZE
            )
        elif event.button == 3:
            self.environment.remove_droplet()
        self.environment_image = World.__environment_to_image(self.environment)
        self.is_updated = True


world = World.random(100)

world.simulate()
