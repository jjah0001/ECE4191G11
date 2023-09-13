import cv2
import time

cap = cv2.VideoCapture(0)
# initialize the cv2 QRCode detector
detector = cv2.QRCodeDetector()

count = 0
wait_time = 5
selected_bin = ""

last_detect_time = time.perf_counter()
while True:
    # detect and decode
    _, img = cap.read()
    data, bbox, _ = detector.detectAndDecode(img)
    cv2.imshow("QRCODEscanner", img)

    # check if there is a QRCode in the image
    if data and time.perf_counter()-last_detect_time >=1:
        if data != selected_bin and selected_bin != "":
            print(f"bin location changed to: {data}")
        else:
            print(f"scanned data: {data}")
        count+= 1
        print(f"parcel count: {count}")
        last_detect_time = time.perf_counter()
        selected_bin = data

    cv2.waitKey(int(1000/60))
    if count >= 1:    
        if time.perf_counter() - last_detect_time >= 5:
            print(f"Moving to Bin {selected_bin}")
            break

cap.release()
cv2.destroyAllWindows()