'''
kinematics class used newtonian Kinematics to find out distance travelled by a mass,
under constant acceleration
'''
import numpy as nn


class kinematics(object):
    '''
    Usage: a = kinematics(delta_time, vector_array, initial_speed_array)
                vector_array: contains effective force vector experienced by any member of the system
                initial_speed_array: this array contains the velocity of every member of the system. which it 
                                      has attained till the last iteration.
    Methods: distance_travelled_array()
            initial_speed_array()
            calc_distance_n_speed_gained()
    '''
    def __init__(self, time_leap, vector_array, initial_speed_array):
        self.distance_gained_array = nn.zeros([len(vector_array)])
        self.time_leapt = time_leap
        self.resultant_vector_array = vector_array
        self.initial_speed_array_ = initial_speed_array

    def distance_travelled_array(self):
        return self.distance_gained_array
    
    def initial_speed_array(self):
        return self.initial_speed_array_

    def calc_distance_n_speed_gained(self):
        for acceleration_index in range(len(self.resultant_vector_array)):
            self.distance_gained_array[acceleration_index] = self.initial_speed_array_[acceleration_index] * self.time_leapt + (
                self.resultant_vector_array[acceleration_index][0] * self.time_leapt**2)/2

            self.initial_speed_array_[acceleration_index] = self.initial_speed_array_[acceleration_index] + \
                self.resultant_vector_array[acceleration_index][0] * \
                self.time_leapt
