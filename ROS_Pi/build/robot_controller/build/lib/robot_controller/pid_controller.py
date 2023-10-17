import RPi.GPIO as GPIO
import math

class Controller:
    def __init__(self, init_speed):
        self.init_speed = init_speed
        # encoder PID errors and initial speed
        self.left_speed = init_speed
        self.right_speed = init_speed
        self.left_prev_error = 0
        self.left_error_sum = 0
        self.right_prev_error = 0
        self.right_error_sum = 0

        # Set up motor speed control
        GPIO.setmode(GPIO.BCM)
        self.en = 25
        GPIO.setup(self.en,GPIO.OUT)
        self.p1=GPIO.PWM(self.en,1000)
        self.p1.start(0)
        self.p1.ChangeDutyCycle(self.right_speed)

        self.en2 = 1
        GPIO.setup(self.en2,GPIO.OUT)
        self.p2=GPIO.PWM(self.en2,1000)
        self.p2.start(0)
        self.p2.ChangeDutyCycle(self.left_speed)
    
    def reset_error(self):
        """
        Method to reset PID errors
        """
        self.left_prev_error = 0
        self.left_error_sum = 0
        self.right_prev_error = 0
        self.right_error_sum = 0

    def correct_speed_KP(self, left_tick, right_tick):
        PID_GAIN = 1
        left_advantage = left_tick - right_tick
        
        # Every two ticks slow down the leading motor by 1 speed
        if left_advantage > 0:
            left_motor_speed = max(self.init_speed - math.floor(left_advantage / (2 / PID_GAIN)), 0)  # Decrease the left motor speed depending on how many ticks ahead the left motor is
            right_motor_speed = self.init_speed
        elif left_advantage < 0:
            left_motor_speed = self.init_speed
            right_motor_speed = max(self.init_speed + math.ceil(left_advantage / (2 / PID_GAIN)), 0)
        else:
            left_motor_speed = self.init_speed
            right_motor_speed = self.init_speed

        self.p2.ChangeDutyCycle(left_motor_speed)
        self.p1.ChangeDutyCycle(right_motor_speed)

    def correct_speed(self, motor, error):
        """
        Method to apply PID control and adjust speed of motors to match a target speed
        """

        if motor == "left":
            
            KP = 0.3 #0.35
            KD = 0.15 #0.1
            KI = 0.04  #0.04

            # self.get_logger().info("error: " + str(error))
            new_speed = self.left_speed + (KP*error) + (KD*self.left_prev_error) + (KI*self.left_error_sum)
            
            if new_speed < 0:
                # self.get_logger().error("Invalid Speed of: " + str(new_speed))
                new_speed = 0
            elif new_speed > 100:
                # self.get_logger().error("Invalid Speed of: " + str(new_speed))
                new_speed = 100

            
            self.left_speed = new_speed
            self.p2.ChangeDutyCycle(new_speed)
            # self.get_logger().info("right wheel speed adjusted to: " + str(self.left_speed))

            self.left_prev_error = error
            self.left_error_sum += error
        
        elif motor == "right":

            KP = 0.3 #0.35
            KD = 0.15 #0.1
            KI = 0.04  #0.04

            # self.get_logger().info("error: " + str(error))
            new_speed = self.right_speed + (KP*error) + (KD*self.right_prev_error) + (KI*self.right_error_sum)
            
            if new_speed < 0:
                # self.get_logger().error("Invalid Speed of: " + str(new_speed))
                new_speed = 0
            elif new_speed > 100:
                # self.get_logger().error("Invalid Speed of: " + str(new_speed))
                new_speed = 100
            
            self.right_speed = new_speed
            self.p1.ChangeDutyCycle(new_speed)
            # self.get_logger().info("right wheel speed adjusted to: " + str(self.right_speed))

            self.right_prev_error = error
            self.right_error_sum += error