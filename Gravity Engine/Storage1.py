import math


class Storage1(object):
    position_coordinates = []  # inputed coordinates storage()
    particles_color = []  # random color generated
    masses = []  # mass of particles
    rendering_state = True  # True - render off, False - renderinging
    multiplier = 1 # Multiplier
    random_mass = False #if mass randomisation is active? True for active
    clock_then_microprocessing_object = [0,0]
    acceleration_label_refrence_storage = []

    def calculating_multiplier(self, dist_btw_farthest_particles):
        longest_distance = 0
        for i in range(len(self.position_coordinates) - 1):
            for j in range(i + 1, len(self.position_coordinates)):
                buff_longest_distance = math.dist(
                    self.position_coordinates[i], self.position_coordinates[j]
                )

                if buff_longest_distance > longest_distance:
                    longest_distance = buff_longest_distance
                    Storage1.multiplier = (dist_btw_farthest_particles / longest_distance)
    
    def position_coordintes_length(self):
        return self.position_coordinates

