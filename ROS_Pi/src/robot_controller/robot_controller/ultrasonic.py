#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import RPi.GPIO as GPIO          
import time
from robot_interfaces.msg import Distances

class Ultrasonic(Node):
    def __init__(self):
        super().__init__("ultrasonic_node") # name of the node in ros2
        
        #GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)
        
        #set GPIO Pins
        self.GPIO_TRIGGER = 27
        self.GPIO_ECHO = 17
        
        #set GPIO direction (IN / OUT)
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)

        self.GPIO_TRIGGER_2 = 2
        self.GPIO_ECHO_2 = 3

        GPIO.setup(self.GPIO_TRIGGER_2, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO_2, GPIO.IN)

        time.sleep(1)
        self.measure_timer = self.create_timer(0.2, self.measure_distance)
        self.measure_publisher = self.create_publisher(Distances, "ultrasonic_distances", 10) # msg type, topic_name to publish to, buffer size

        self.get_logger().info("Ultrasonic class initiallised")

    def measure_distance(self):
        msg = Distances()
        msg.sensor1 = float(self.get_average_distance(0))
        time.sleep(0.01)
        msg.sensor2 = float(self.get_average_distance(1))
        time.sleep(0.01)
        msg.sensor3 = float(self.get_average_distance(2))

        # self.get_logger().info("Publishing ultrasonic distances: ( Sensor 1: " + str(msg.sensor1) + ", Sensor 2: " + str(msg.sensor2) + ")")
        self.measure_publisher.publish(msg)


    def get_distance(self, sensor):
        if sensor == 0:
            trig = self.GPIO_TRIGGER
            echo = self. GPIO_ECHO
        elif sensor ==1:
            trig = self.GPIO_TRIGGER_2
            echo = self. GPIO_ECHO_2
        elif sensor == 2:
            return 0.0

        # set Trigger to HIGH
        GPIO.output(trig, True)
    
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(trig, False)
    
        StartTime = time.time()
        StopTime = time.time()
    
        no_echo = False
        # save StartTime
        start_start_time = StartTime
        while GPIO.input(echo) == 0:
            if time.time() - start_start_time > 0.2: 
                break
            StartTime = time.time()
    
        if not no_echo:
            # save time of arrival
            while GPIO.input(echo) == 1:
                StopTime = time.time()
    
    
        
            # time difference between start and arrival
            TimeElapsed = StopTime - StartTime
            # multiply with the sonic speed (34300 cm/s)
            # and divide by 2, because there and back
            # self.get_logger().info("time between emission and detection: " + str(TimeElapsed))
            distance = (TimeElapsed * 34300) / 2
            # self.get_logger().info("distance recorded: " + str(distance))
            if distance >= 200:
                return -999.0
            return distance
        else:
            return -999.0

    
    def get_average_distance(self, sensor):
        distance_array = []
        for i in range(3):
            dist = self.get_distance(sensor)

            if dist > 0 and dist < 200:
                distance_array.append(dist)
            
            length = len(distance_array)
            if length == 0:
                return 0
            else:
                return sum(distance_array)/length

    
    def test_continuous_reading(self):
        # self.get_logger().info("Ultrasonic would return distance continuously")
        try:
            while True:
                dist = self.get_distance()
                self.get_logger().info("Measured Distance =" + str(dist) +" cm")
                time.sleep(0.1)
            # Reset by pressing CTRL + C
        except KeyboardInterrupt:
            self.get_logger().warning("Measurement stopped by User")
            GPIO.cleanup()


def main(args=None):
    try:
        rclpy.init(args=args)
        ultrasonic_node = Ultrasonic()
        rclpy.spin(ultrasonic_node)

    except KeyboardInterrupt:
        ultrasonic_node.get_logger().info("drive node shutdown")
    rclpy.shutdown()


if __name__ == "__main__": # If you want to run node from terminal directly
    main()
