import numpy as nn

class Feeder(object):
    def __init__(self, mass_array, multiplier, *position_coordinates) -> None:
        self.position_coordinates_ = nn.array([i for i in list(zip(position_coordinates[0],position_coordinates[1]))])
        self.multiplier_ = multiplier
        self.mass_array_ = nn.array(mass_array)
        self.initial_speed_array_ = nn.zeros([len(self.position_coordinates_)])
        self.multiplying_multiplier()

    def multiplying_multiplier(self):
        self.position_coordinates_ = self.position_coordinates_ * self.multiplier_
    
    def multiplier(self):
        return self.multiplier_

    def no_of_particles(self):
        return len(self.position_coordinates_)

    def position_coordinates(self):
        return self.position_coordinates_
    
    def mass_array(self):
        return self.mass_array_
    
    def initial_speed_array(self):
        return self.initial_speed_array_

    def set_position_coordinates(self, position_coordinates):
        self.position_coordinates_ = position_coordinates

    def set_mass_array(self, mass_array):
        self.mass_array_ = mass_array

    def set_initial_speed_array(self, inital_speed_array):
        self.initial_speed_array_ = inital_speed_array
    

