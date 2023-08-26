import RPi.GPIO as GPIO
from rclpy.node import Node
import rclpy
import time
from robot_interfaces.msg import EncoderInfo

class Encoder(Node):
    def __init__(self):
        super().__init__("encoder_node")
        self.get_logger().info("Encoder node initialised")
        self.left_count = 0
        self.right_count = 0
        self.left_state = '00'
        self.right_state = '00'
        self.left_vel = 0
        self.right_vel = 0

        GPIO.setmode(GPIO.BCM)
        self.left_wheel_ena = 5
        self.left_wheel_enb = 6
        GPIO.setup(self.left_wheel_ena, GPIO.IN)
        GPIO.setup(self.left_wheel_enb, GPIO.IN)


        self.right_wheel_ena = 16
        self.right_wheel_enb = 26
        GPIO.setup(self.right_wheel_ena, GPIO.IN)
        GPIO.setup(self.right_wheel_enb, GPIO.IN)

        self.runEncoder = True

        self.encoder_publisher = self.create_publisher(EncoderInfo, "encoder_info", 10) # msg type, topic_name to publish to, buffer size

    def detectEncoder(self):
        # sample_freq = 3000
        # period = 1/sample_freq
        # t = time.time()

        reset_time = True
        while True:
            # t += period
            # track time
            if reset_time:
                start_time = time.time()
                reset_time = False

                prev_left_count = self.left_count
                prev_right_count = self.right_count


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
            elapsed_time = time.time() - start_time 
            if (elapsed_time >= 0.1):
                self.left_vel = (self.left_count - prev_left_count)/elapsed_time #vel in cps, counts per sec
                self.right_vel = (self.right_count - prev_right_count)/elapsed_time
                reset_time = True
            # publish msg
            msg = EncoderInfo()
            msg.left_count = int(self.left_count)
            msg.right_count = int(self.right_count)
            msg.left_vel = float(self.left_vel)
            msg.right_vel = float(self.right_vel)
            self.encoder_publisher.publish(msg)
            # self.get_logger().info("COUNT_ENC: (" + str(msg.left_count) + ", " + str(msg.right_count) + ")")

            # time.sleep(max(0,t-time.time()))

def main(args=None):
    try:
        rclpy.init(args=args)

        encoder_node = Encoder()
        encoder_node.detectEncoder()
        rclpy.spin(encoder_node)

    except KeyboardInterrupt:
        encoder_node.clear_gpio()
        encoder_node.get_logger().info("Encoder node shutdown")
    rclpy.shutdown()


if __name__ == "__main__":
    main()


