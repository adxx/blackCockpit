# -*- coding: utf-8 -*-


import os
import sys
from threading import Thread
import time
import datetime


from kivy.app import App
from kivy.properties import NumericProperty
from kivy.properties import BoundedNumericProperty
from kivy.properties import StringProperty
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import Scatter
from kivy.uix.stencilview import StencilView
from kivy.animation import Animation
from kivy.config import Config

#Config.set('graphics', 'resizable', True)

os.environ['KIVY_GL_BACKEND'] = 'gl'
os.environ['KIVY_WINDOW'] = 'egl_rpi'


class PropertyState(object):
    def __init__(self, last, current):
        self.last = last
        self.current = current

    def last_is_not_now(self):
        return self.last is not self.current


class Dashboard(FloatLayout):
    def __init__(self, **kwargs):
        super(Dashboard, self).__init__(**kwargs)

        # Background
        self.background_image = Image(source='bg.png')
        self.add_widget(self.background_image)

        # RPM
        self.rpm = Gauge(file_gauge="gauge512.png", do_rotation=False, do_scale=False, do_translation=False, value=0,
                         size_gauge=512, pos=(72, -16))
        self.add_widget(self.rpm)
        self.rpm.value = 700

        # Speedometer
        self.speedometer = Label(text='180', font_size=80, font_name='hemi_head_bd_it.ttf', pos=(274,194))
        self.rpm.add_widget(self.speedometer)

        # BOTTOM BAR
        self.bottom_bar = Image(source='bottomBar.png', pos=(0, -209))
        self.add_widget(self.bottom_bar)

        # KM LEFT
        self.km_left_label = Label(text='000', font_name='Avenir.ttc', halign="right", text_size=self.size,
                                   font_size=32, pos=(260, 234))
        self.add_widget(self.km_left_label)

        # CLOCK
        self.clock = Label(text='00:00', font_name='Avenir.ttc', halign="right", text_size=self.size, font_size=32,
                           pos=(-130, -180))
        self.add_widget(self.clock)

        # OUTDOOR TEMPERATURE
        self.outdoor_temperature_label = Label(text='00.0', font_name='Avenir.ttc', halign="right", text_size=self.size,
                                               font_size=32, pos=(95, -180))
        self.add_widget(self.outdoor_temperature_label)
        self.unitC = Label(text='°C', font_name='Avenir.ttc', halign="left", text_size=self.size, font_size=24,
                           pos=(200, -172))
        self.add_widget(self.unitC)

        # OIL TEMPERATURE
        self.oil_label = Label(text='0', font_name='Avenir.ttc', halign="right", text_size=self.size, font_size=27,
                               pos=(-390, -180))
        self.add_widget(self.oil_label)

        # DISTANCE
        self.distance_label = Label(text='000000', font_name='Avenir.ttc', halign="right", text_size=self.size,
                                    font_size=27, pos=(305, -180))
        self.add_widget(self.distance_label)

        # FUEL CONSUMPTION
        self.fuel_consumption_label = Label(text='00.0', font_name='Avenir.ttc', halign="right", text_size=self.size,
                                     font_size=32, pos=(-290, 234))
        self.add_widget(self.fuel_consumption_label)

        # COOLANT TEMPERATURE
        self.coolant_bar = StencilView(size_hint=(None, None), size=(94, 256), pos=(15, 112))
        self.coolant_image = Image(source='coolantScaleFull.png', size=(94, 256), pos=(15, 112))
        self.coolant_bar.add_widget(self.coolant_image)
        self.add_widget(self.coolant_bar)
        self.coolant_bar.height = 100

        # FUEL LEFT
        self.fuel_bar = StencilView(size_hint=(None, None), size=(94, 256), pos=(686, 112))
        self.fuel_image = Image(source='fuelScaleFull.png', size=(94, 256), pos=(686, 112))
        self.fuel_bar.add_widget(self.fuel_image)
        self.add_widget(self.fuel_bar)
        self.fuel_bar.height = 100

        # CAR DOORS
        #self.car = Car(pos=(257, 84))
        #self.add_widget(self.car)
        #self.minimize_car()

    def minimize_car(self):
        anim = Animation(scale=0.5, opacity=0,  t='linear', duration=0.5)
        anim.start(self.car)

        anim_rpm = Animation(scale=1, opacity=1, t='linear', duration=0.5)
        anim_rpm.start(self.rpm)

    def maximize_car(self):
        anim = Animation(scale=1, opacity=1,  t='linear', duration=0.5)
        anim.start(self.car)

        anim_rpm = Animation(scale=0.5, opacity=0, t='linear', duration=0.5)
        anim_rpm.start(self.rpm)


class Car(Scatter):
    car_image = StringProperty("car362/car.png")

    driver_door_closed_image = StringProperty("car362/driverClosedDoor.png")
    driver_door_opened_image = StringProperty("car362/driverOpenedDoor.png")

    passenger_door_closed_image = StringProperty("car362/passangerClosedDoor.png")
    passenger_door_opened_image = StringProperty("car362/passangerOpenedDoor.png")

    left_door_closed_image = StringProperty("car362/leftClosedDoor.png")
    left_door_opened_image = StringProperty("car362/leftOpenedDoor.png")

    right_door_closed_image = StringProperty("car362/rightClosedDoor.png")
    right_door_opened_image = StringProperty("car362/rightOpenedDoor.png")

    doors_states = NumericProperty(0)

    size = (286, 362)

    def __init__(self, **kwargs):
        super(Car, self).__init__(**kwargs)

        _car = Image(source=self.car_image, size=self.size)

        self.driver_door_opened = Image(source=self.driver_door_opened_image, size=self.size)
        self.passenger_door_opened = Image(source=self.passenger_door_opened_image, size=self.size)
        self.left_door_opened = Image(source=self.left_door_opened_image, size=self.size)
        self.right_door_opened = Image(source=self.right_door_opened_image, size=self.size)

        self.driver_door_closed = Image(source=self.driver_door_closed_image, size=self.size)
        self.passenger_door_closed = Image(source=self.passenger_door_closed_image, size=self.size)
        self.left_door_closed = Image(source=self.left_door_closed_image, size=self.size)
        self.right_door_closed = Image(source=self.right_door_closed_image, size=self.size)

        self.add_widget(_car)
        self.add_widget(self.driver_door_opened)
        self.add_widget(self.passenger_door_opened)
        self.add_widget(self.left_door_opened)
        self.add_widget(self.right_door_opened)

        self.bind(doors_states=self._update)

    def _update(self, *args):
        driver_door_states = self.doors_states & 1
        passenger_door_states = self.doors_states & 4
        left_door_states = self.doors_states & 16
        right_door_states = self.doors_states & 64
        if driver_door_states != 0:
            try:
                self.remove_widget(self.driver_door_opened)
                self.add_widget(self.driver_door_closed)
            except:
                pass
        else:
            try:
                self.remove_widget(self.driver_door_closed)
                self.add_widget(self.driver_door_opened)
            except:
                pass
        if passenger_door_states != 0:
            try:
                self.remove_widget(self.passenger_door_opened)
                self.add_widget(self.passenger_door_closed)
            except:
                pass
        else:
            try:
                self.remove_widget(self.passenger_door_closed)
                self.add_widget(self.passenger_door_opened)
            except:
                pass
        if left_door_states != 0:
            try:
                self.remove_widget(self.left_door_opened)
                self.add_widget(self.left_door_closed)
            except:
                pass
        else:
            try:
                self.remove_widget(self.left_door_closed)
                self.add_widget(self.left_door_opened)
            except:
                pass
        if right_door_states != 0:
            try:
                self.remove_widget(self.right_door_opened)
                self.add_widget(self.right_door_closed)
            except:
                pass
        else:
            try:
                self.remove_widget(self.right_door_closed)
                self.add_widget(self.right_door_opened)
            except:
                pass


class Gauge(Scatter):
    value = NumericProperty(10)  # BoundedNumericProperty(0, min=0, max=360, errorvalue=0)
    size_gauge = BoundedNumericProperty(512, min=128, max=512, errorvalue=128)
    size_text = NumericProperty(10)
    file_gauge = StringProperty("")

    def __init__(self, **kwargs):
        super(Gauge, self).__init__(**kwargs)

        self._gauge = Scatter(
            size=(self.size_gauge, self.size_gauge),
            do_rotation=False,
            do_scale=False,
            do_translation=False
        )

        _img_gauge = Image(source=self.file_gauge, size=(self.size_gauge, self.size_gauge))

        self._needle = Scatter(
            size=(self.size_gauge, self.size_gauge),
            do_rotation=False,
            do_scale=False,
            do_translation=False
        )

        _img_needle = Image(source="arrow512.png", size=(self.size_gauge, self.size_gauge))

        self._gauge.add_widget(_img_gauge)
        self._needle.add_widget(_img_needle)

        self.add_widget(self._gauge)
        self.add_widget(self._needle)

        self.bind(pos=self._update)
        self.bind(size=self._update)
        self.bind(value=self._turn)

    def _update(self, *args):
        self._gauge.pos = self.pos
        self._needle.pos = (self.x, self.y)
        self._needle.center = self._gauge.center

    def _turn(self, *args):
        self._needle.center_x = self._gauge.center_x
        self._needle.center_y = self._gauge.center_y
        self._needle.rotation = 112-(0.028*self.value)  # 1 rpm = 0.028 gr



class BoxApp(App):
    def build(self):
        dashboard = Dashboard()
        #listener = CanListener(dashboard)
        #can.Notifier(bus, [listener])

        return dashboard


if __name__ == "__main__":
    # Send requests
    #RequestsLoop()

    _old_excepthook = sys.excepthook

    def myexcepthook(exctype, value, traceback):
        if exctype == KeyboardInterrupt:
            print ("Handler code goes here")
        else:
            _old_excepthook(exctype, value, traceback)
    sys.excepthook = myexcepthook

    # Show dashboard
    BoxApp().run()
