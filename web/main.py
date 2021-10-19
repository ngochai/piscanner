from RpiMotorLib import RpiMotorLib
from flask import Flask, render_template_string, redirect, request, Response
from time import sleep

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
#HTML Code 
TPL = '''
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">                
        <title>Stepper Motor Controller</title>
    </head>
    <body>
    </body>
</html>
'''
 
@app.route("/")
def home():
    return render_template_string(TPL)
    
@app.route("/m1")
def m1():
    cw = True if request.args.get("cw") == '1' else False
    step = int(request.args.get("step"))
    print("Cw: ", cw, ", step: ", step)
    motor1.motor_go(cw, "Full", step, .01, False, .05)
    return Response(status = 200)
     
@app.route("/m2")
def m2():
    cw = True if request.args.get("cw") == '1' else False
    step = int(request.args.get("step") )
    print("Cw: ", cw, ", step: ", step)
    motor2.motor_go(cw, "Full", step, .01, False, .05)
    return Response(status = 200)
 
# Run the app on the local development server
if __name__ == "__main__":
    app.run(host='0.0.0.0' , port=5000)