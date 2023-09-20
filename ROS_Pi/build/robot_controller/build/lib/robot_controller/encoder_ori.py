import RPi.GPIO as GPIO
from rclpy.node import Node
import rclpy
import time
from robot_interfaces.msg import EncoderInfo
import matplotlib.pyplot as plt

class Encoder(Node):
    def __init__(self):
        super().__init__("encoder_node")
        self.left_count = 0
        self.right_count = 0
        self.left_state = '00'
        self.right_state = '00'
        self.left_vel = 0
        self.right_vel = 0

        self.left_speed = 70
        self.right_speed = 70

        self.left_prev_error = 0
        self.left_error_sum = 0
        self.right_prev_error = 0
        self.right_error_sum = 0

        GPIO.setmode(GPIO.BCM)
        self.left_wheel_ena = 5
        self.left_wheel_enb = 6
        GPIO.setup(self.left_wheel_ena, GPIO.IN)
        GPIO.setup(self.left_wheel_enb, GPIO.IN)


        self.right_wheel_ena = 16
        self.right_wheel_enb = 26
        GPIO.setup(self.right_wheel_ena, GPIO.IN)
        GPIO.setup(self.right_wheel_enb, GPIO.IN)

        self.encoder_publisher = self.create_publisher(EncoderInfo, "encoder_info", 10) # msg type, topic_name to publish to, buffer size

        self.left_speed_arr = []
        self.right_speed_arr = []
        
        # Setting up GPIO
        time.sleep(2)
        GPIO.setmode(GPIO.BCM)
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

        self.get_logger().info("Encoder node initialised")

        self.start_graph_time = time.perf_counter()
        self.set_speed = True
        self.target_cps = 1600
        self.target_speed_arr = []

    def detectEncoder(self):
        # sample_freq = 3000
        # period = 1/sample_freq
        # t = time.perf_counter()

        reset_time = True
        while True:
            # t += period
            # track time
            if reset_time:
                start_time = time.perf_counter()
                reset_time = False

                prev_left_count = self.left_count
                prev_right_count = self.right_count


            # self.get_logger().info(f"left pwm: {self.left_speed}, right pwm: {self.right_speed}")
            # self.get_logger().info(f"left en: {self.left_count}, right en: {self.right_count}")
            # check encoder
            lp1 = GPIO.input(self.left_wheel_ena)
            lp2 = GPIO.input(self.left_wheel_enb)
            left_newState = "{}{}".format(lp1, lp2)

            if self.left_state != left_newState:
                self.left_count += 1
                self.left_state = left_newState

            rp1 = GPIO.input(self.right_wheel_ena)
            rp2 = GPIO.input(self.right_wheel_enb)
            right_newState = "{}{}".format(rp1, rp2)

            if self.right_state != right_newState:
                self.right_count += 1
                self.right_state = right_newState

            # calc velocity
            elapsed_time = time.perf_counter() - start_time 
            if (elapsed_time >= 0.1):

                self.left_vel = (self.left_count - prev_left_count)/elapsed_time #vel in cps, counts per sec
                self.right_vel = (self.right_count - prev_right_count)/elapsed_time
                self.left_speed_arr.append(self.left_vel)
                self.right_speed_arr.append(self.right_vel)


                if len(self.target_speed_arr) < 3:
                    self.target_speed_arr.append(self.left_vel)
                else:
                    self.target_speed_arr.pop(0)
                    self.target_speed_arr.append(self.left_vel)

                
                if self.set_speed and self.left_vel > 1000 and all(abs(x - self.target_speed_arr[0]) <100 for x in self.target_speed_arr ):
                    
                    self.target_cps = sum(self.target_speed_arr)/len(self.target_speed_arr)
                    self.set_speed = False
                    self.get_logger().info(f"target cps: {self.target_cps}")

                if self.set_speed == False:
                    if self.left_vel >= self.target_cps - 400 or self.right_vel >= self.target_cps - 400:
                        try:
                            error_left = 100 * (self.target_cps- self.left_vel)/self.target_cps
                        except ZeroDivisionError:
                            error_left = 0
                        try:
                            error_right = 100 * (self.target_cps - self.right_vel)/self.target_cps
                        except ZeroDivisionError:
                            error_right = 0

                        if abs(error_left) >= 1 and abs(error_left) < 50:
                            self.correct_speed("left", error_left)

                        if abs(error_right) >= 1 and abs(error_right) < 50:
                            self.correct_speed("right", error_right)


                reset_time = True
            # publish msg
            msg = EncoderInfo()
            msg.left_count = int(self.left_count)
            msg.right_count = int(self.right_count)
            self.encoder_publisher.publish(msg)
            # self.get_logger().info("COUNT_ENC: (" + str(msg.left_count) + ", " + str(msg.right_count) + ")")

            # time.sleep(max(0,t-time.perf_counter()))

            if time.perf_counter() - self.start_graph_time >= 60:
                self.get_logger().info("graph done")
                plt.figure()
                plt.plot(self.left_speed_arr)
                plt.legend(["left"])
                plt.savefig('left_encoder.png')
                plt.close()
                plt.figure()
                plt.plot(self.right_speed_arr)
                plt.legend(["right"])
                plt.savefig("right_encoder.png")
                plt.close()
                self.start_graph_time = time.perf_counter() + 999999


    def correct_speed(self, motor, error):
        """
        This function will adjust the right wheel speed so that it matches the left speed
        """

        if motor == "left":
            
            KP = 0.1   #0.1
            KD = 0.0
            KI = 0.02  #0.02

            # self.get_logger().info("error: " + str(error))
            new_speed = self.left_speed + (KP*error) + (KD*self.left_prev_error) + (KI*self.left_error_sum)
            if new_speed < 0 or  new_speed > 100:
                self.get_logger().error("Invalid Speed of: " + str(new_speed))
                raise Exception("Invalid Speed of: " + str(new_speed))
            
            self.left_speed = new_speed
            self.p2.ChangeDutyCycle(new_speed)
            # self.get_logger().info("right wheel speed adjusted to: " + str(self.left_speed))

            self.left_prev_error = error
            self.left_error_sum += error
        
        elif motor == "right":

            KP = 0.1  #0.1
            KD = 0.0
            KI = 0.02  #0.02

            # self.get_logger().info("error: " + str(error))
            new_speed = self.right_speed + (KP*error) + (KD*self.right_prev_error) + (KI*self.right_error_sum)
            if new_speed < 0 or  new_speed > 100:
                self.get_logger().error("Invalid Speed of: " + str(new_speed))
                raise Exception("Invalid Speed of: " + str(new_speed))
            
            self.right_speed = new_speed
            self.p1.ChangeDutyCycle(new_speed)
            # self.get_logger().info("right wheel speed adjusted to: " + str(self.right_speed))

            self.right_prev_error = error
            self.right_error_sum += error

def main(args=None):
    try:
        rclpy.init(args=args)

        encoder_node = Encoder()
        encoder_node.detectEncoder()
        rclpy.spin(encoder_node)

    except KeyboardInterrupt:
        encoder_node.get_logger().info("Encoder node shutdown")

    rclpy.shutdown()


if __name__ == "__main__":
    main()


