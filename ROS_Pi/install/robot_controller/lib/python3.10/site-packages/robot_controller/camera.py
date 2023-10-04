import cv2
import time 
import sys

sys.path.insert(1, '/home/rpi-team11/ECE4191G11/ROS_Pi/src/robot_controller/robot_controller')

from led import LED

class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        # initialize the cv2 QRCode detector
        self.detector = cv2.QRCodeDetector()

        ##### initialise LED #####
        self.led = LED()

    def read_qr(self):
        """
        Method to read image frames from camera and detect qr code until a qr code has been detected
        """
        count = 0
        wait_time = 5
        selected_bin = 0
        led_change_time = time.perf_counter()

        last_detect_time = time.perf_counter()
        while True:
            try:

                # detect and decode
                _, img = self.cap.read()
                data, bbox, _ = self.detector.detectAndDecode(img)
                # cv2.imshow("QRCODEscanner", img)

                # check if there is a QRCode in the image
                if data and time.perf_counter()-last_detect_time >=1:

                    if data != selected_bin and selected_bin != 0:
                        print(f"bin location changed to: {data}")
                    else:
                        print(f"scanned data: {data}")
                    count+= 1
                    last_detect_time = time.perf_counter()
                    selected_bin = data
                    
                    self.led.turn_on()
                    time.sleep(0.2)
                    self.led.turn_off()

                if count >= 1:    
                    if time.perf_counter() - last_detect_time >= wait_time:
                        print(f"Moving to Bin {selected_bin}")
                        return int(selected_bin)
                else:
                    ## LED flash
                    if time.perf_counter() - led_change_time >= 0.5:
                        self.led.flash()
                        led_change_time = time.perf_counter()

            except Exception as e:
                print(e)