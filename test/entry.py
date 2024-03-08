import cv2
from paddleocr import PaddleOCR
from collections import Counter
import csv
import time

ocr = PaddleOCR(use_angle_cls=True, lang="korean")
cap = cv2.VideoCapture(0)

def save(text):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open('parking.csv', 'a', encoding='utf-8', newline='') as file:
        csv.writer(file).writerow([text, timestamp])
    print(f"데이터 '{text}' 저장됨.")

min_width, min_height = 100, 50
captured_texts, should_continue = [], True

while should_continue:
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
            save(most_common_text)
            should_continue = False  # 중복 텍스트가 10번 이상 나타나면 반복 종료

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
