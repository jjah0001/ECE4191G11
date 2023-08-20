from drive import Drive
import time
import RPi.GPIO as GPIO          
from ultrasonic import Ultrasonic

left_wheel_ena = 5
left_wheel_enb = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(left_wheel_ena, GPIO.IN)
GPIO.setup(left_wheel_enb, GPIO.IN)

def drive(speed, distance):
    controller = Drive()
    controller.drive_forwards(speed)

    # 170mm per revolution, per 3600 count
    WHEEL_CIRCUMFERENCE = 169
    COUNTS_PER_REV = 3600
    total_count = 0
    deg = 0
    count_required = (distance/WHEEL_CIRCUMFERENCE)*COUNTS_PER_REV
    input_a = 0
    input_b = 0

    print(count_required)

    while total_count < count_required:
        if GPIO.input(left_wheel_ena) != input_a or GPIO.input(left_wheel_enb) != input_b:
            input_a = GPIO.input(left_wheel_ena)
            input_b = GPIO.input(left_wheel_enb)

            total_count += 1
            deg = total_count/10
            print(deg)
            distance_travelled = total_count*(WHEEL_CIRCUMFERENCE/COUNTS_PER_REV)
            print(str(distance_travelled) + "mm")
    controller.stop()
    controller.clear_gpio()

ultrasonic_1 = Ultrasonic()

while True:
    print(ultrasonic_1.get_distance())
    time.sleep(0.01)






