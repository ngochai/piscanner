from sys import stderr
from RpiMotorLib import RpiMotorLib
from flask import Flask, render_template, redirect, request, Response
from time import sleep
import os
import logging
import subprocess

import gphoto2 as gp

path = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(filename='/var/log/piscannerweb.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

#Nema 17 Stepper Motor 42x23 17HS4023
m1_GPIO_pins = (14, 15, 18) # Microstep Resolution MS1-MS3 -> GPIO Pinm1_
m1_direction= 20       # Direction -> GPIO Pin
m1_step = 21      # Step -> GPIO Pin
motor1 = RpiMotorLib.A4988Nema(m1_direction, m1_step, m1_GPIO_pins, "A4988")

m2_GPIO_pins = (2, 3, 4) # Microstep Resolution MS1-MS3 -> GPIO Pin
m2_direction= 17       # Direction -> GPIO Pin
m2_step = 27      # Step -> GPIO Pin
motor2 = RpiMotorLib.A4988Nema(m2_direction, m2_step, m2_GPIO_pins, "A4988")


app = Flask(__name__)

def runcommand(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #return result.stdout.decode('utf-8')
    return result.stdout

 
@app.route("/")
def home():      
    return render_template('index.html')
    
@app.route("/m1")
def m1():
    cw = True if request.args.get("cw") == '1' else False
    step = int(request.args.get("step"))
    app.logger.debug("Cw: ", cw, ", step: ", step)
    motor1.motor_go(cw, "Full", step, .01, False, .05)
    return Response(status = 200)
     
@app.route("/m2")
def m2():
    cw = True if request.args.get("cw") == '1' else False
    step = int(request.args.get("step") )
    app.logger.debug("Cw: ", cw, ", step: ", step)
    motor2.motor_go(cw, "Full", step, .01, False, .05)
    return Response(status = 200)
 
@app.route("/takephoto")
def takephoto():    
    camera = gp.Camera()
    camera.init()
    app.logger.debug('Capturing image')
    file_path = camera.capture(gp.GP_CAPTURE_IMAGE)
    target_dir = os.path.join(path, 'static', 'images', 'cam')
    os.makedirs(target_dir)
    target_file = os.path.join(target_dir, 'output.jpg')
    app.logger.debug('Copying image to', target_file)
    camera_file = camera.file_get(
        file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
    camera_file.save(target_file)
    camera.exit()
    return Response(status = 200)


# Run the app on the local development server
if __name__ == "__main__":
    app.run(host='0.0.0.0' , port=5000)