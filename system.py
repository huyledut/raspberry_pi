import cv2
import RPi.GPIO as GPIO
import time
import requests

GPIO.setmode(GPIO.BCM)
BASE_ORIGIN = 'https://af53-118-69-73-134.ngrok-free.app'
DETECTION_URL = f'{BASE_ORIGIN}/api/v1/object-to-json'
# Chọn GPIO 4 để đọc giá trị từ module PNP E3F-DS30P1
sensor_pin = 4
# Khởi tạo camera
camera = cv2.VideoCapture(0)
# Thiết lập kích thước khung hình của camera
camera.set(3, 640) # set chiều rộng khung hình
camera.set(4, 640) # set chiều cao khung hình

# Thiết lập GPIO 17 là input
GPIO.setup(sensor_pin, GPIO.IN)

while True:
    # Đọc giá trị từ module PNP E3F-DS30P1
    value = GPIO.input(sensor_pin)

    if value == GPIO.LOW:
        print("Object detected")
        cv2.destroyAllWindows()
        # Chụp ảnh
        ret, frame = camera.read()
        IMAGE_URL = "detect.jpg"
        cv2.imwrite(IMAGE_URL, frame)
        with open(IMAGE_URL, 'rb') as f:
            image_data = f.read()
        response = requests.post(DETECTION_URL, files={'file' : image_data}).json()
        print(response)
        try:
            for result in response:
                xmin = int(result['xmin'])
                ymin = int(result['ymin'])
                xmax = int(result['xmax'])
                ymax = int(result['ymax'])
                label = str(round(result['confidence'] * 100)) + '% ' + result['name']
                color = (0, 255, 0) # màu xanh lá cây
                thickness = 2
                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, thickness)

                # css
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.5 # tỷ lệ kích thước của chữ
                text_color = (0, 255, 0) # màu xanh lá cây
                text_thickness = 2 # độ dày của chữ
                text_size, _ = cv2.getTextSize(label, font, font_scale, text_thickness)

                cv2.putText(frame, label, (xmin, ymin - text_size[1]), font, font_scale, text_color, text_thickness)
        except Exception as e:
            print(e)
        cv2.imshow('Windows', frame)
        cv2.waitKey(2000)
        # Giải phóng tài nguyên
        cv2.destroyAllWindows()
    else:
        print("No object detected")

    # Chờ 0.5 giây trước khi đọc lại giá trị từ module
    time.sleep(0.5)

# Giải phóng tài nguyên camera
camera.release()