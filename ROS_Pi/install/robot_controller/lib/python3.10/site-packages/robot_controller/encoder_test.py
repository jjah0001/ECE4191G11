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


        self.prev_time_l = 0
        self.prev_time_r = 0


    def detectEncoder(self):
        # sample_freq = 3000
        # period = 1/sample_freq
        # t = time.perf_counter()

        self.prev_time_l = time.perf_counter()
        self.prev_time_r = time.perf_counter()
        reset_time = True
        while True:
            # t += period
            # track time
            if reset_time:
                start_time = time.perf_counter()
                reset_time = False




            # check encoder
            lp1 = GPIO.input(self.left_wheel_ena)
            lp2 = GPIO.input(self.left_wheel_enb)
            left_newState = "{}{}".format(lp1, lp2)
            self.left_vel = 0
            if self.left_state != left_newState:
                if self.left_count == 0:
                    self.left_count = 1
                else:
                    self.left_count += 1
                    self.left_state = left_newState
                    curr_t_l = time.perf_counter()
                    dt_l = curr_t_l - self.prev_time_l
                    if dt_l:
                        self.left_vel = 1/dt_l
                        self.left_speed_arr.append(self.left_vel)
                    self.prev_time_l = curr_t_l



            rp1 = GPIO.input(self.right_wheel_ena)
            rp2 = GPIO.input(self.right_wheel_enb)
            right_newState = "{}{}".format(rp1, rp2)
            self.right_vel = 0
            if self.right_state != right_newState:
                if self.right_count ==0:
                    self.right_count = 1
                else:
                    self.right_count += 1
                    self.right_state = right_newState
                    curr_t_r = time.perf_counter()
                    dt_r = curr_t_r - self.prev_time_r
                    if dt_r < 1:
                        self.right_vel = 1/dt_r
                        self.right_speed_arr.append(self.right_vel)
                    self.prev_time_r = curr_t_r



            # calc velocity
            elapsed_time = time.perf_counter() - start_time 
            if (elapsed_time >= 0.1):

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
                        error_left = self.target_cps- self.left_vel
                        error_right = self.target_cps - self.right_vel
                        
                        self.correct_speed("left", error_left)
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
            
            KP = 0.01   #0.1
            KD = 0.0
            KI = 0.0  #0.02

            self.get_logger().info("left error: " + str(error))
            new_speed = self.left_speed + min(max((KP*error) + (KD*self.left_prev_error) + (KI*self.left_error_sum), 0), 50)
            new_speed = min(max(new_speed, 0), 95)

            self.left_speed = new_speed
            self.p2.ChangeDutyCycle(new_speed)
            # self.get_logger().info("right wheel speed adjusted to: " + str(self.left_speed))

            self.left_prev_error = error
            self.left_error_sum += error
        
        elif motor == "right":
        
            KP = 0.01  #0.1
            KD = 0.0
            KI = 0.0  #0.02

            self.get_logger().info("right error: " + str(error))
            new_speed = self.right_speed + min(max((KP*error) + (KD*self.right_prev_error) + (KI*self.right_error_sum), 0), 50)
            new_speed = min(max(new_speed, 0), 95)
            
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


