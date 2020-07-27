import numpy
import matplotlib.pyplot as plt
from environment import Environment
from bacteria import Bacteria

class Simulation:
	
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
        environment = Environment(Simulation.L, Simulation.DROPLET_SIZE)
        bacterias = [
            Bacteria.random(environment, Simulation.VELOCITY)
            for _ in range(number_bacterias)
        ]
        environment_image = Simulation.__environment_to_image(environment)
        return Simulation(environment, bacterias, environment_image)
        
    @staticmethod
    def __environment_to_image(environment):
        image = numpy.zeros((Simulation.OUTPUT_IMAGE_SIZE, Simulation.OUTPUT_IMAGE_SIZE))
        for x in range(Simulation.OUTPUT_IMAGE_SIZE):
            for y in range(Simulation.OUTPUT_IMAGE_SIZE):
                image[y,x] = environment.density(
                    x*environment.L/Simulation.OUTPUT_IMAGE_SIZE,
                    y*environment.L/Simulation.OUTPUT_IMAGE_SIZE
                )
        return image
    
    def run(self):
        t = 0
        while True:
            self.draw(t)
            for bacteria in self.bacterias:
                bacteria.update(self.environment, Simulation.DT)
            t += Simulation.DT

    def draw(self, t):
        image = self.environment_image.copy()
        for bacteria in self.bacterias:
            x = int((bacteria.x*Simulation.OUTPUT_IMAGE_SIZE/self.environment.L))
            y = int((bacteria.y*Simulation.OUTPUT_IMAGE_SIZE/self.environment.L))
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
                event.xdata*self.environment.L/Simulation.OUTPUT_IMAGE_SIZE,
                event.ydata*self.environment.L/Simulation.OUTPUT_IMAGE_SIZE
            )
        elif event.button == 3:
            self.environment.remove_droplet()
        self.environment_image = Simulation.__environment_to_image(self.environment)
        self.is_updated = True
