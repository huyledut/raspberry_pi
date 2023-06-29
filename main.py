import serial
import cv2
import time
import requests
import pprint
import warnings
from speech2 import ts

warnings.filterwarnings("ignore")

ser = serial.Serial("/dev/ttyUSB0", 9600)
ser.reset_input_buffer()
BASE_ORIGIN = 'http://34.143.164.207:8000/'
DETECTION_URL = f'{BASE_ORIGIN}api/v1/object-to-json'
# Khởi tạo camera
camera = cv2.VideoCapture(0)
# Thiết lập kích thước khung hình của camera
camera.set(3, 640) # set chiều rộng khung hình
camera.set(4, 640) # set chiều cao khung hình

state = None
while state != 'Start':
    state = input("Nhap 'Start' de bat dau!\n")

ser.write(state.encode())

while True:
    if  ser.inWaiting()>0: 
        data = ser.readline().decode().strip()
        if data == "Started":
            break 
        print(data)
    print("123")
    time.sleep(1)

try:
    ser.reset_input_buffer()
    while True:
        if  ser.inWaiting()>0: 
            data = ser.readline()
        else:
            continue
        data = data.decode("utf-8").strip()
        print(data)
        if data == "A":
            ser.flushInput()
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
            try:
                response = requests.post(DETECTION_URL, files={'file': image_data}).json()
                # result detection
                res_detect = set()
                for result in response:
                    xmin = int(result['xmin'])
                    ymin = int(result['ymin'])
                    xmax = int(result['xmax'])
                    ymax = int(result['ymax'])
                    label = str(round(result['confidence'] * 100)) + '% ' + result['name']
                    res_detect.add(result['name'])
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
            except Exception as e:
                print(str(e))
                send_data = "B"
                ser.write(send_data.encode())
                time.sleep(2)
                continue
            # read result
            text = "Kết quả kiểm tra:"
            if len(res_detect):
                text += " Xuất hiện lỗi"
                for item in res_detect:
                    text += f'{item}, '
            else:
                text += "Vải không xuất hiện lỗi!"

            # save result
            print("step 3")
            cv2.imwrite("result.jpg", image)
            pprint.pprint(response)
            
            ts.Read(text)
            time.sleep(1)
            print("step 4")
            # send data arduino
            send_data = "B"
            ser.write(send_data.encode())

            time.sleep(2)
except KeyboardInterrupt:
    ser.close()