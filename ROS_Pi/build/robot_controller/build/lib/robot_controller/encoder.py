import RPi.GPIO as GPIO
import rclpy
from rclpy.node import Node
from robot_interfaces.msg import EncoderInfo

class Encoder(Node):
    def __init__(self):
        super().__init__("encoder_node")
        # encoder state and counts
        self.left_count = 0
        self.right_count = 0
        self.left_state = [0, 0]
        self.right_state = [0, 0]


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

        self.encoder_publisher = self.create_publisher(EncoderInfo, "encoder_info", 10)

    def update_encoder_loop(self):
        """
        Method that indefinately updates encoder counts
        """
        while True:
            state_changed = False
            # check encoder
            lp1 = GPIO.input(self.left_wheel_ena)
            lp2 = GPIO.input(self.left_wheel_enb)

            if self.left_state[0] != lp1 or self.left_state[1] != lp2:
                self.left_count += 1
                self.left_state = [lp1, lp2]
                state_changed = True

            rp1 = GPIO.input(self.right_wheel_ena)
            rp2 = GPIO.input(self.right_wheel_enb)

            if self.right_state[0] != rp1 or self.right_state[1] != rp2:
                self.right_count += 1
                self.right_state = [rp1, rp2]
                state_changed = True
            
            if self.left_count %1000 ==0 and self.left_count > 100:
                print(self.left_count, self.right_count)
            
            if state_changed:
                msg = EncoderInfo()
                msg.left_count = int(self.left_count)
                msg.right_count = int(self.right_count)
                self.encoder_publisher.publish(msg)

    def reset_encoder_counts(self):
        """
        Method to reset encoder counts
        """
        self.left_count = 0
        self.right_count = 0

def main(args=None):
    try:
        rclpy.init(args=args)

        encoder_node = Encoder()
        encoder_node.update_encoder_loop()
        rclpy.spin(encoder_node)

    except KeyboardInterrupt:
        encoder_node.get_logger().info("Encoder node shutdown")

    rclpy.shutdown()


if __name__ == "__main__":
    main()