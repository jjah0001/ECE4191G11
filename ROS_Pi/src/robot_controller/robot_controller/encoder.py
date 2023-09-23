import RPi.GPIO as GPIO

class Encoder:
    def __init__(self):
        # encoder state and counts
        self.left_count = 0
        self.right_count = 0
        self.left_state = [0, 0]
        self.right_state = [0, 0]

        # encoder PID errors and initial speed
        self.left_speed = 60
        self.right_speed = 60
        self.left_prev_error = 0
        self.left_error_sum = 0
        self.right_prev_error = 0
        self.right_error_sum = 0

        # GPIO set up
        GPIO.setmode(GPIO.BCM)
        self.left_wheel_ena = 5
        self.left_wheel_enb = 6
        GPIO.setup(self.left_wheel_ena, GPIO.IN)
        GPIO.setup(self.left_wheel_enb, GPIO.IN)


        self.right_wheel_ena = 16
        self.right_wheel_enb = 26
        GPIO.setup(self.right_wheel_ena, GPIO.IN)
        GPIO.setup(self.right_wheel_enb, GPIO.IN)
        
        self.en = 25
        GPIO.setup(self.en,GPIO.OUT)
        self.p1=GPIO.PWM(self.en,1000)
        self.p1.start(0)
        self.p1.ChangeDutyCycle(self.left_speed)

        self.en2 = 1
        GPIO.setup(self.en2,GPIO.OUT)
        self.p2=GPIO.PWM(self.en2,1000)
        self.p2.start(0)
        self.p2.ChangeDutyCycle(self.right_speed)

    def update_encoder_loop(self):
        """
        Method that indefinately updates encoder counts
        """
        while True:
            # check encoder
            lp1 = GPIO.input(self.left_wheel_ena)
            lp2 = GPIO.input(self.left_wheel_enb)

            if self.left_state[0] != lp1 or self.left_state[1] != lp2:
                self.left_count += 1
                self.left_state = [lp1, lp2]

            rp1 = GPIO.input(self.right_wheel_ena)
            rp2 = GPIO.input(self.right_wheel_enb)

            if self.right_state[0] != rp1 or self.right_state[1] != rp2:
                self.right_count += 1
                self.right_state = [rp1, rp2]
            
            if self.left_count %1000 ==0 and self.left_count > 100:
                print(self.left_count, self.right_count)

    def reset_encoder_counts(self):
        """
        Method to reset encoder counts
        """
        self.left_count = 0
        self.right_count = 0

    def reset_error(self):
        """
        Method to reset PID errors
        """
        self.left_prev_error = 0
        self.left_error_sum = 0
        self.right_prev_error = 0
        self.right_error_sum = 0

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