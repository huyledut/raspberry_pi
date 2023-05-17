import serial

ser = serial.Serial("/dev/ttyUSB0", 9600)
import cv2
import time
import requests
import pprint
import warnings
warnings.filterwarnings("ignore")

BASE_ORIGIN = 'https://ff08-2402-800-6294-3859-b0a0-15b3-6089-210d.ngrok-free.app'
DETECTION_URL = f'{BASE_ORIGIN}/api/v1/object-to-json'
# Khởi tạo camera
camera = cv2.VideoCapture(0)
# Thiết lập kích thước khung hình của camera
camera.set(3, 640) # set chiều rộng khung hình
camera.set(4, 640) # set chiều cao khung hình

try:
    while True:
        # recieve signal arduino
        # ser.reset_input_buffer()
        if  ser.inWaiting()>0: 
            data = ser.readline()
            # ser.flushInput() #remove data after readin
        else:
            continue
        data = data.decode("utf-8").strip()
        print(data)
        if data == "A":
            # take a sample photo
            print("step 1")
            ret, frame = camera.read()
            IMAGE_URL = "detect.jpg"
            cv2.imwrite(IMAGE_URL, frame)
            with open(IMAGE_URL, 'rb') as f:
                image_data = f.read()
            image = cv2.imread(IMAGE_URL)

            # call api to detect
            print("step 2")
            response = requests.post(DETECTION_URL, files={'file': image_data}).json()
            # result detection
            for result in response:
                xmin = int(result['xmin'])
                ymin = int(result['ymin'])
                xmax = int(result['xmax'])
                ymax = int(result['ymax'])
                label = str(round(result['confidence'] * 100)) + '% ' + result['name']
                color = (0, 255, 0) # màu xanh lá cây
                thickness = 2
                cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, thickness)

                # css
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.5 # tỷ lệ kích thước của chữ
                text_color = (0, 255, 0) # màu xanh lá cây
                text_thickness = 2 # độ dày của chữ
                text_size, _ = cv2.getTextSize(label, font, font_scale, text_thickness)

                cv2.putText(image, label, (xmin, ymin - text_size[1]), font, font_scale, text_color, text_thickness)
            
            # save result
            print("step 3")
            cv2.imwrite("result.jpg", image)
            pprint.pprint(response)

            # send data arduino
            print("step 4")
            send_data = "B"
            ser.write(send_data.encode())
            time.sleep(2)
except KeyboardInterrupt:
    ser.close()