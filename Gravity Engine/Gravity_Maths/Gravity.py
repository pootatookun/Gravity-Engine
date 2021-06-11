'''
gravity class uses Newton's law of universal gravitation, and calulates force of ttraction 
between two masses
'''
import numpy as nn

G = 6.67*(10**-11)

class gravity(object):
    '''
    Usage: a = gravity(no_of_particles, mass_array)
                mass_array: row matrice of mass of every particle
    Methods: calc_acceleration_array()
             acceleration_array()
    '''

    def __init__(self, no_of_particles, mass_array):
        self.length = no_of_particles
        self.acceleration_ = nn.empty([self.length, self.length - 1])
        self.mass_array = mass_array
        
    def calc_acceleration_array(self, iterating_distance_array):
        '''
        Usage: object.acceleration_array(iterating_distance_array)
               iterating_distance_array: distance array i.e distance between every particle
        to calculate acceleration between every particle, caused by universal law of gravitation.
        '''
        self.acceleration_ = nn.square(nn.reciprocal(iterating_distance_array)) * G

        for i in range(self.length):
            temp_mass_buffer = nn.delete(nn.copy(self.mass_array), i)
            self.acceleration_[i] = self.acceleration_[i] * temp_mass_buffer
        
            
    def acceleration_array(self):
        return self.acceleration_
