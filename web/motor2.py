#from flask import Flask, render_template_string, request 
from time import sleep
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib

#define GPIO pins
GPIO_pins = (2, 3, 4) # Microstep Resolution MS1-MS3 -> GPIO Pin
direction= 17       # Direction -> GPIO Pin
step = 27      # Step -> GPIO Pin

# Declare an named instance of class pass GPIO pins numbers
mymotortest = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988")


mymotortest.motor_go(False, "Full" , 10, .01, True, .05)
