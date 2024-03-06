import cv2
from paddleocr import PaddleOCR
from collections import Counter
import csv
import time

# OCR 객체 초기화
ocr = PaddleOCR(use_angle_cls=True, lang="korean")
cap = cv2.VideoCapture(0)

def in_and_out(target):
    """파일에서 target 텍스트의 존재 여부에 따라 추가하거나 삭제"""
    rows = []
    found = False
    try:
        with open('parking.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                # 중복된 데이터 발견 시 삭제
                if row[0] == target:
                    found = True
                    continue
                rows.append(row)
    except FileNotFoundError:
        print("파일이 존재하지 않습니다.")

    # 중복되지 않은 경우 새로운 데이터 추가
    if not found:
        timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        rows.append([target, timestamp_str])

    # 파일에 변경사항 적용
    with open('parking.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    
    action = "삭제" if found else "추가"
    print(f"'{target}' 데이터가 {action}되었습니다.")

min_width, min_height = 100, 50
captured_texts = []

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        result = ocr.ocr(frame, cls=True)
        texts = [info[1][0] for line in result if line for info in line if info[1][1] > 0.5 and info[0][2][0] - info[0][0][0] >= min_width and info[0][2][1] - info[0][0][1] >= min_height]

        if texts:
            combined_text = ''.join(texts)
            captured_texts.append(combined_text)
            text_counter = Counter(captured_texts)
            most_common_text, count = text_counter.most_common(1)[0]
            if count >= 10:
                in_and_out(most_common_text)
                break  # 조건을 만족하면 루프 종료

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cap.release()
    cv2.destroyAllWindows()
