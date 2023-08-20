import RPi.GPIO as GPIO          
from time import sleep
import logging
import time

class Drive():
    def __init__(self):


        logging.info('Drive class initialised')

        # Setting up GPIO
        self.in1 = 23
        self.in2 = 24
        self.en = 25
        #GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.in1,GPIO.OUT)
        GPIO.setup(self.in2,GPIO.OUT)
        GPIO.setup(self.en,GPIO.OUT)
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)
        self.p1=GPIO.PWM(self.en,1000)



        self.in3 = 7
        self.in4 = 8
        self.en2 = 1

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.in3,GPIO.OUT)
        GPIO.setup(self.in4,GPIO.OUT)
        GPIO.setup(self.en2,GPIO.OUT)
        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.LOW)
        self.p2=GPIO.PWM(self.en2,1000)

    def _set_speed(self, motor, direction, speed):
        """
        Set speed and direction for selected motor

        :param motor:  Either 0 or 1 to select motor
        :param direction: "forward" or "reverse"
        :param speed: 0-100%
        
        """
        logging.info("Motor " + str(motor) + " selected to move "  + str(direction) + " and with speed " + str(speed))
        if speed < 0 or speed > 100:
            logging.error("The speed is invalid")
            raise Exception("Invalid speed")

        if motor == 0:
            if direction == "forward":
                self.p1.start(0)
                self.p1.ChangeDutyCycle(speed)
                GPIO.output(self.in1,GPIO.HIGH)
                GPIO.output(self.in2,GPIO.LOW)
            elif direction == "reverse":
                self.p1.start(0)
                self.p1.ChangeDutyCycle(speed)
                GPIO.output(self.in1,GPIO.LOW)
                GPIO.output(self.in2,GPIO.HIGH)
            else:
                logging.error("The direction is invalid")
                raise Exception("Invalid direction")
            
        elif motor == 1:
            if direction == "forward":
                self.p2.start(0)
                self.p2.ChangeDutyCycle(speed)
                GPIO.output(self.in3,GPIO.HIGH)
                GPIO.output(self.in4,GPIO.LOW)
            elif direction == "reverse":
                self.p2.start(0)
                self.p2.ChangeDutyCycle(speed)
                GPIO.output(self.in3,GPIO.LOW)
                GPIO.output(self.in4,GPIO.HIGH)
            else:
                logging.error("The direction is invalid")
                raise Exception("Invalid direction")
            
        else:
            logging.error("The motor is invalid")
            raise Exception("Invalid motor selected")
        
    def _stop_motor(self, motor):
        if motor == 0:
            GPIO.output(self.in1,GPIO.LOW)
            GPIO.output(self.in2,GPIO.LOW)
            self.p1.stop()
        elif motor == 1:
            GPIO.output(self.in3,GPIO.LOW)
            GPIO.output(self.in4,GPIO.LOW)
            self.p2.stop()
        else:
            logging.error("The motor is invalid")
            raise Exception("Invalid motor selected")
    
    def rotate(self, direction, speed):
        """
        Rotate at a specified speed in either direction
        :param direction: "CW" or "CCW"
        :param speed: 0-100%
        """
        logging.info("Robot rotates " + direction + " with Input speed: " + str(speed))
        if speed < 0 or speed > 100:
            logging.error("The speed is invalid")
            raise Exception("Invalid speed")

        if direction == "CCW":
            logging.info("Rotating CCW")
            self._set_speed(0, "forward", speed)
            self._set_speed(1, "reverse", speed)
        elif direction == "CW":
            logging.info("Rotating CW")
            self._set_speed(0, "reverse", speed)
            self._set_speed(1, "forward", speed)
        else:
            logging.info("Invalid direction")
            raise Exception("Invalid direction")
        
    def drive_forwards(self, speed, duration=None):
        """
        Drive forwards at a specified speed. If duration is given, stops after a certain time
        
        """
        logging.info("Robot drives forward with Input speed: " + str(speed) + " Input duration: " + str(duration))
        if speed < 0 or speed > 100:
            logging.error("The speed is invalid")
            raise Exception("Invalid speed")
        
        self._set_speed(0, "forward", speed)
        self._set_speed(1, "forward", speed)

        if (duration is not None):
            if isinstance(duration, int) or isinstance(duration, float):
                time.sleep(duration)
                self._stop_motor(0)
                self._stop_motor(1)
            else:
                logging.error("The duration is invalid")
                raise Exception("Invalid duration")
        
    def drive_backwards(self, speed, duration=None):
        logging.info("Robot drives backwards with Input speed: " + str(speed) + " Input duration: " + str(duration))
        if speed < 0 or speed > 100:
            logging.error("The speed is invalid")
            raise Exception("Invalid speed")
        
        self._set_speed(0, "reverse", speed)
        self._set_speed(1, "reverse", speed)

        if (duration is not None):
            if isinstance(duration, int) or isinstance(duration, float):
                time.sleep(duration)
                self._stop_motor(0)
                self._stop_motor(1)
            else:
                logging.error("The duration is invalid")
                raise Exception("Invalid duration")
    
    def stop(self):
        logging.info("Motor stopped")
        self._stop_motor(0)
        self._stop_motor(1)

    def drive_distance(self, distance):
        """
        Calibrate this to find the correct time + speed % = what distance

        distance = vel * time, calibrate what speed % = what velocity?        
        
        """

        pass

    def clear_gpio(self):
        GPIO.cleanup()
