import multiprocessing as mp

from Storage1 import *
from Gravity_Maths.Vector import vectors
from Gravity_Maths.Gravity import gravity
from Gravity_Maths.Kinematics import kinematics
from Gravity_Maths.Feeder import Feeder



class M_storage(object):
    def __init__(self) -> None:
        self.position_coordinates_x = 0
        self.position_coordinates_y = 0
        self.time_elapsed = mp.Value('d',0)
        self.acceleration_ = 0 


    def position_coordinates(self):
        return self.position_coordinates_x, self.position_coordinates_y

    def set_position_coordinate(self, position_coordinates):
        self.position_coordinates_x = mp.Array("i", len(position_coordinates))
        self.position_coordinates_y = mp.Array("i", len(position_coordinates))

        for i in range(len(position_coordinates)):
            self.position_coordinates_x[i] = position_coordinates[i][0]
            self.position_coordinates_y[i] = position_coordinates[i][1]

    def set_acceleration(self, length):
        self.acceleration_ = mp.Array("d", length)

    def get_acceleration(self):
        return self.acceleration_

    def get_time_elapsed(self):
        return self.time_elapsed
    
        

    
    



