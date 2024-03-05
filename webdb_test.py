from flask import Flask, jsonify, render_template, request, redirect, send_file, url_for, Response
from werkzeug.utils import secure_filename, send_from_directory
import os
import subprocess
import sys
import csv
import time
sys.path.append('./utils')
app = Flask(__name__)
app.id_count = 1
app.users = {}

@app.route('/carwork', methods=['GET','POST'])
def detect():
 #yolov5를 커스텀한 코드
    if __name__ == "__main__":
        app.run() #app.run(port='5001') 5001번포트로의 접속을 허용한다는 뜻, 설정을 해주지 않으면 default 포트번호 5000번

    return "testrun"

@app.route('/carin', methods=['GET','POST'])
def come():
    new_user            = request.json
    new_user["id"]         = app.id_count
    app.users[app.id_count] = new_user
    app.id_count         = app.id_count + 1
    return jsonify(new_user)


def check_duplicate_and_save(target, timestamp_str):
    # 파일이 존재하는지 확인하고, 존재하면 읽어서 중복 검사
    duplicate_found = False
    try:
        with open('example.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == target:
                    duplicate_found = True
                    break
    except FileNotFoundError:
        # 파일이 존재하지 않으면 중복이 없는 것으로 처리
        pass

    # 중복이 없을 경우 데이터 저장
    if not duplicate_found:
        with open('example.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([target, timestamp_str])

        print("데이터가 파일에 저장되었습니다.")
        return file
    else:
        print("중복된 데이터가 있습니다. 저장하지 않습니다.")

def entry(car_num):
    timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
    print("Timestamp:", timestamp_str)
    target_vehicle = car_num
    check_duplicate_and_save(target_vehicle, timestamp_str)
    car_print = car_num + ", " + timestamp_str
    return car_print

@app.route('/carread', methods=['GET','POST'])
def car_read():
    car_data = entry("aaa5677")
    return jsonify(car_data)

@app.route('/cardata', methods=['GET','POST'])
def car_datas():
    car_data = entry("aaa5677")
    return car_data