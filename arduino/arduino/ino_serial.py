import serial
import time
import sys
import tty
import termios


# 아두이노와의 시리얼 통신 설정 (포트 및 전송 속도)
arduino_port = '/dev/ttyACM0'  # 아두이노 포트에 맞게 변경
baud_rate = 9600

# 아두이노와 시리얼 통신 시작
ser = serial.Serial(arduino_port, baud_rate)
time.sleep(2)  # 아두이노가 시리얼 통신을 시작할 시간을 기다립니다.

print("init")

while True:    
    # 사용자로부터 문자열을 입력받음
    c = input("입력 :")
    
    if c == 'q':
        break
    
    # 아두이노로 문자열을 전송
    ser.write(c.encode())
    print("메시지를 전송했습니다:", c)