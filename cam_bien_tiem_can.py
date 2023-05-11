import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Chọn GPIO 4 để đọc giá trị từ module PNP E3F-DS30P1
sensor_pin = 4

# Thiết lập GPIO 17 là input
GPIO.setup(sensor_pin, GPIO.IN)

while True:
    # Đọc giá trị từ module PNP E3F-DS30P1
    value = GPIO.input(sensor_pin)

    if value == GPIO.HIGH:
        print("No object detected")
    else:
        print("Object detected")

    # Chờ 0.5 giây trước khi đọc lại giá trị từ module
    time.sleep(0.5)