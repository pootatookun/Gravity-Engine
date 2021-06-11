'''
Following Class takes care of all the Vectors/Coordinate Geometry
for the Gravity Engine.
it provides varies functions to calculate and retrieve: slope, effective component,
                                                        resultant vector, final coordinates
of the provided Coordinates(in my case we can say Particles)
'''

import math 
import numpy as nn


class vectors(object):
    '''
    Usage: a = vectors(Coordinate_array) :- 'Coordinate_array': python list of cartesian coordinates of 
                                            form [[x1,y1], [x2,y2], [x3,y3],.......].
    Methods: get_coordinate_array(); slope_array()
             effective_component_array(); resultant_vector_array()
             final_coordinates_array(); set_coordinate_array()
             distance_array()
             calc_distance_array()
             calc_slopeArray()
             effective_component_array()

                                            
    '''
    nn.set_printoptions(precision=15)

    def __init__(self, coordinate_array):
        self.coordinate_array = coordinate_array
        self.length = len(self.coordinate_array)
        self.distance_array_ = nn.empty([self.length, self.length - 1]) 
        self.slope_array_ = nn.empty([self.length, self.length - 1])
        self.effective_component_array_ = nn.empty([self.length, 2])
        self.resultant_vector_array_ = nn.empty([self.length, 2])
        self.final_coordinates_array_ = nn.empty([self.length, 2])
        
    def get_coordinate_array(self):
        '''
        returns the latest coordinate array of the system
        '''
        return self.coordinate_array

    def slope_array(self):
        '''
        returns calultes slope of coordinates
        '''
        return self.slope_array_

    def effective_component_array(self):
        '''
        returns effective component array
        '''
        return self.effective_component_array_

    def resultant_vector_array(self):
        '''
        returns resultant vector array
        '''
        return self.resultant_vector_array_

    def final_coordinates_array(self):
        '''
        return new coordinae array
        '''
        return self.final_coordinates_array_
    
    def set_coordinate_array(self, coordinate_array):
        '''
        updating variable self.coordinate_array, which was given coordinates by user initally, to
        new calculated coordinates
        '''
        self.coordinate_array = coordinate_array
    
    def distance_array(self):
        return self.distance_array_

    def calc_distance_array(self):
        '''
        calc distance between every coordinate in Coordinate_array.
        '''
        for i in range(self.length-1):
            for j in range(i+1, self.length):
                self.distance_array_[i][j-1] = math.dist(self.coordinate_array[i], self.coordinate_array[j])
                self.distance_array_[j][i] = self.distance_array_[i][j-1]

    def calc_slopeArray(self):
        '''
        calc slopes between each point in Coordinate_array
        '''
        displacement_vec = nn.empty([self.length, self.length - 1, 2])

        for i in range(self.length-1):
            for j in range(i+1, self.length):
                displacement_vec[i][j-1] = self.coordinate_array[j] -  self.coordinate_array[i]
                displacement_vec[j][i] = displacement_vec[i][j-1] * -1 + 0

                self.slope_array_[
                    i][j-1] = math.atan2(displacement_vec[i][j-1][1], displacement_vec[i][j-1][0])
                self.slope_array_[j][i] = math.atan2(
                    displacement_vec[j][i][1], displacement_vec[j][i][0])

        two_pi_array = 6.2831853071795 * nn.ones(self.slope_array_.shape)
        nn.add(two_pi_array, self.slope_array_,
               out=self.slope_array_, where=self.slope_array_ < 0)

    def calc_effective_component_array(self, Vector):
        '''
        calclates effective x and y components of 'Vector'
        (which in my case is accelartion between each particle)
        '''

        cos_component_array = nn.cos(self.slope_array_)
        sin_component_array = nn.sin(self.slope_array_)
        nn.around(cos_component_array, 10, out=cos_component_array)
        nn.around(sin_component_array, 10, out=sin_component_array)
        cos_component_array += 0 # zero is added to remove condition of 
        sin_component_array += 0 # '-0'. which may arise in float numbers.

        cos_component_array *= Vector
        sin_component_array *= Vector

        cos_component_array = nn.vstack(nn.sum(cos_component_array, axis=1)) # summing cos and sin component and
        sin_component_array = nn.vstack(nn.sum(sin_component_array, axis=1)) # converting them into column matrices.
        self.effective_component_array_ = nn.concatenate(
            (cos_component_array, sin_component_array), axis=1)

    def calc_resultant_vector_array(self):
        '''
        calulates the resultant from effective_component_array, which is stored 
        at zeroth index of every row. And at First index, resultant slope is stored
        '''
        for count, components in enumerate(self.effective_component_array_):
            self.resultant_vector_array_[count][0] = math.hypot(
                components[0], components[1])
            buff_resultant_slope = math.atan2(components[1], components[0])
            if buff_resultant_slope < 0:
                buff_resultant_slope += 6.283185 #atan2 result is between -pi/2 and pi/2. 
                                                 # 6.283185 is 360 degrees. adding with every negative angle value,
                                                 # convert them into equivalent positive angles.
            self.resultant_vector_array_[count][1] = buff_resultant_slope

    def calc_final_coordinates_array(self, distance_gained_array):
        '''
        updating coordinates feeded at the start.
        x is added with x component 
        y with y component
        '''
        resultant_array_slope = nn.hstack(self.resultant_vector_array_)[1::2]#convertes to row matrice, then took out every
                                                                             # second element(which is resulatant slope). 

        cos_component_array = nn.cos(resultant_array_slope) * distance_gained_array
        sin_component_array = nn.sin(resultant_array_slope) * distance_gained_array

        cos_component_array = nn.vstack(cos_component_array)
        sin_component_array = nn.vstack(sin_component_array)

        self.final_coordinates_array_ = self.coordinate_array + \
            nn.concatenate((cos_component_array, sin_component_array), axis=1)
            