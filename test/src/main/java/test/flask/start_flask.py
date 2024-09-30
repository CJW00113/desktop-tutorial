from flask import Flask, Response, request, jsonify, render_template

import logging
import requests  # Spring Boot 서버와 통신을 위해 requests 모듈 사용
import os
from flask_cors import CORS
import cv2
import subprocess


# app = Flask(__name__)
app = Flask(__name__, template_folder='src/main/resources/templates/flask')

# Spring Boot의 출처 허용
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:9090"}})
# CORS(app, origins="http://localhost:9090")  # Spring Boot 서버의 출처를 지정
CORS(app)

# 로그 설정
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return render_template('slider_display.html')  # 새로운 HTML 페이지를 렌더링


@app.route('/api/slider', methods=['POST', 'OPTIONS'])
def slider():
    if request.method == 'OPTIONS':
        return '', 200  # CORS preflight 요청에 대한 응답
    data = request.get_json()  # JSON 데이터 받기
    if data:  # 데이터가 존재하는지 확인
        value = data.get('value')  # 슬라이더 값 가져오기
        print(f"Received slider value: {value}")  # 로그 출력
    else:
        print("No data received")  # 데이터가 없을 경우 로그 출력
    return jsonify({'value': value})  # JSON 응답


# @app.route('/api/slider', methods=['POST', 'OPTIONS'])
# def slider():
#     if request.method == 'OPTIONS':
#         return '', 200  # CORS preflight 요청에 대한 응답
#     data = request.get_json()  # JSON 데이터 받기
#     value = data.get('value')  # 슬라이더 값 가져오기
#     # 터미널에 슬라이더 값 출력
#     print(f"Received slider value: {value}")
#     return jsonify({'value': value})  # JSON 응답

# @app.route('/api/slider', methods=['GET'])
# def get_slider_value():
#     # Spring Boot 서버에서 슬라이더 값을 가져오는 요청
#     try:
#         response = requests.get('http://localhost:9090/api/slider')  # Spring Boot 서버의 실제 URL로 변경
#         slider_value = response.json().get('value', '값 없음')
#         return jsonify({'value': slider_value})
#     except Exception as e:
#         logging.error(f'Error fetching slider value: {e}')
#         return jsonify({'value': '오류 발생'})


process = None

app = Flask(__name__)

def generate_frames():
    print("1")
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break

        # 프레임에 글자 추가
        cv2.putText(frame, 'Hello, World!', (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, 
                    (255, 0, 0), 2)

        # JPEG로 인코딩
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def run_script():
    global process
    process = subprocess.Popen(['python', 'hello.py'])  # 실행할 스크립트 경로

if __name__ == '__main__':
    logging.info("Starting Flask server on port 8080...")
    app.run(port=8080)