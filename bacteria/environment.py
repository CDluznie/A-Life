import numpy

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
