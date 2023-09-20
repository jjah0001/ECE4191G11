import cv2
import time 

class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        # initialize the cv2 QRCode detector
        self.detector = cv2.QRCodeDetector()

    def read_qr(self):
        self.detect_timer.cancel()

        count = 0
        wait_time = 5
        selected_bin = 0

        last_detect_time = time.perf_counter()
        while True:
            # detect and decode
            _, img = self.cap.read()
            data, bbox, _ = self.detector.detectAndDecode(img)
            # cv2.imshow("QRCODEscanner", img)

            # check if there is a QRCode in the image
            if data and time.perf_counter()-last_detect_time >=1:
                if data != selected_bin and selected_bin != 0:
                    self.get_logger().info(f"bin location changed to: {data}")
                else:
                    self.get_logger().info(f"scanned data: {data}")
                count+= 1
                last_detect_time = time.perf_counter()
                selected_bin = data

            if count >= 1:    
                if time.perf_counter() - last_detect_time >= wait_time:
                    self.get_logger().info(f"Moving to Bin {selected_bin}")
                    return int(selected_bin)