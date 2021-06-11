from MP_storage import *
import numpy as nn

def calc_particles_states(acceleration_array ,time_elapsed, mass_array, multiplier, position_coordinate_x, position_coordinate_y):

    fed = Feeder(mass_array, multiplier, position_coordinate_x, position_coordinate_y)
    inputs = vectors(fed.position_coordinates())
    acc = gravity(fed.no_of_particles(), fed.mass_array())

    while(True):
        inputs.calc_distance_array()
        inputs.calc_slopeArray()
        acc.calc_acceleration_array(inputs.distance_array())
        inputs.calc_effective_component_array(acc.acceleration_array())
        inputs.calc_resultant_vector_array()

        for i in range(len(inputs.resultant_vector_array())):
            acceleration_array[i] = inputs.resultant_vector_array()[i][0]

        distance = kinematics(
            0.001, inputs.resultant_vector_array(), fed.initial_speed_array()
        )
        time_elapsed.value = round(time_elapsed.value + 0.001, 3)
        distance.calc_distance_n_speed_gained()
        fed.set_initial_speed_array(distance.initial_speed_array())
        inputs.calc_final_coordinates_array(distance.distance_travelled_array())
        inputs.set_coordinate_array(inputs.final_coordinates_array())

        buff_final_position_array = inputs.final_coordinates_array() / fed.multiplier()
        nn.around(buff_final_position_array, out=buff_final_position_array)
        buff_final_position_array = inputs.final_coordinates_array() / fed.multiplier()
        for i in range(len(buff_final_position_array)):
            position_coordinate_x[i] = int(buff_final_position_array[i][0])
            position_coordinate_y[i] = int(buff_final_position_array[i][1])

def microprocessor_main_start():
    mp_storage.set_position_coordinate(Storage1.position_coordinates)
    mp_storage.set_acceleration(len(Storage1.position_coordinates))
    p = mp.Process(
        target=calc_particles_states, args=(mp_storage.get_acceleration() ,mp_storage.get_time_elapsed(), Storage1.masses, Storage1.multiplier , *mp_storage.position_coordinates())
    )
    Storage1.clock_then_microprocessing_object[1] = p
    p.start()

if __name__ == '__main__':
    
    mp.freeze_support() 
    from Kivy_import import *
    
    Window.maximize()
    
    class Mass(Popup):
        mass = ObjectProperty(None)

        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        def mass_(self):
            Storage1.masses.append(int(self.mass.text))
            return self.dismiss()


    class Engine_controls_n_info(BoxLayout):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        def distance_farthest(self):
            Storage1().calculating_multiplier(int(self.ids.farthest_distance.text))

        def button_state(self):
            if Storage1.rendering_state and  len(Storage1.position_coordinates) > 1: # to make sure, atleast two points are marked
                self.ids.begin_fun.background_color = (1,0,0)
                Storage1.rendering_state = False # disabling marking of points on particle renderer
                self.mass_acceleration_info()
                microprocessor_main_start()
                event = Clock.schedule_interval(self.parent.ids.particle_renderer.game_begins, 1.0/60.0)
                Storage1.clock_then_microprocessing_object[0] = event

        def random_mass(self):
            if not Storage1.random_mass:
                Storage1.random_mass = True
                self.ids.random_mass.background_color = 0,1,0
            else:
                Storage1.random_mass = False
                self.ids.random_mass.background_color = 1,0,0
    
        def mass_acceleration_info(self):
            for i in range(len(Storage1.masses)):
                mass = Label(text=str(Storage1.masses[i])+'Kg', markup=True,size_hint_y=None, height=40, size_hint_x=None, width=90)
                acc = Label(text=str(mp_storage.get_acceleration()), size_hint_y=None, height=40)
                Storage1.acceleration_label_refrence_storage.append(acc)
                self.ids.scroll_view.add_widget(mass)
                self.ids.scroll_view.add_widget(acc)

        def exit(self, touch):
            if touch.is_double_tap and self.ids.exit.collide_point(touch.x, touch.y):
                if mp.active_children():
                    Storage1.clock_then_microprocessing_object[1].terminate()
                    Storage1.clock_then_microprocessing_object[1].join()
                    Storage1.clock_then_microprocessing_object[1].close()
                App.get_running_app().stop()

    """ 
    Particles are rendered here. 
    Input for the particles. any relevant calculations
    dimensions start pos: root window's i.e. 0,0
    size: 4/5 of root windows , root window's height
    """


    class Particle_Renderer(BoxLayout):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

    # to take particle input
        def on_touch_down(self, touch):
            if  Storage1.rendering_state and self.collide_point(touch.x, touch.y):
                with self.canvas:
                    Color(*self.random_no_generator(), mode="hsv")
                    d = radius
                    Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
                Storage1.position_coordinates.append([round(touch.x), round(touch.y)])
            
                if Storage1.random_mass:
                    Storage1.masses.append(randrange(0,900000000))

            return super().on_touch_down(touch)

        def on_touch_up(self, touch):
            if Storage1.rendering_state and not Storage1.random_mass and self.collide_point(touch.x, touch.y):
                Factory.Mass().open()
            return super().on_touch_up(touch)

        def random_no_generator(self):
            """
            returns three random numbes, to be used to color Ellipse,
            when taking inputs
            """
            random_storage = round(random(), 4), 1, 1

            if random_storage not in Storage1.particles_color:
                Storage1.particles_color.append(random_storage)
                return random_storage

        def mass_update_acceleration(self):
            for i in range(len(Storage1.acceleration_label_refrence_storage)):
                Storage1.acceleration_label_refrence_storage[i].text = str(mp_storage.get_acceleration()[i])+'m/s\u00b2'
       
        def game_begins(self, dt):
            self.canvas.clear()
            k = mp_storage.position_coordinates()  # this i smore effecient
            for i in range(len(Storage1.position_coordinates)):
                with self.canvas:
                    Color(*Storage1.particles_color[i], mode="hsv")
                    d = radius
                    Ellipse(pos=(k[0][i], k[1][i]), size=(d, d))
            self.parent.ids.info_renderer.ids.time_elapsed.text = str(mp_storage.get_time_elapsed().value)
            self.mass_update_acceleration()

        """ Root Window"""


    class Gravity_engine_layout(Widget):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        """clear particle renderer canvas and all stored value"""

        def reload(self):
            Clock.unschedule(Storage1.clock_then_microprocessing_object[0])
            if mp.active_children():
                Storage1.clock_then_microprocessing_object[1].terminate()
                Storage1.clock_then_microprocessing_object[1].join()
                Storage1.clock_then_microprocessing_object[1].close()
            self.ids.particle_renderer.canvas.clear()
            Storage1.position_coordinates = []
            Storage1.particles_color = []
            Storage1.masses = []
            Storage1.rendering_state = True
            Storage1.random_mass = False
            Storage1.multiplier = 1
            Storage1.clock_then_microprocessing_object = [0,0]
            self.ids.info_renderer.ids.random_mass.background_color = 1,0,0
            self.ids.info_renderer.ids.begin_fun.background_color = 0,1,0
            mp_storage.time_elapsed.value = 0 
            self.ids.info_renderer.ids.scroll_view.clear_widgets()
            Storage1.acceleration_label_refrence_storage = []
           
            


        """Root App"""


    class Gravity_engineApp(App):
        
        def build(self):
            return Gravity_engine_layout()



        """Main run Loop"""
    radius = 35
    mp_storage = M_storage()
    Gravity_engineApp().run()
    
