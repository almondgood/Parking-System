import cv2
from paddleocr import PaddleOCR
from collections import Counter
import csv
import time

ocr = PaddleOCR(use_angle_cls=True, lang="korean")
cap = cv2.VideoCapture(0)

def exit(target):
    # 임시 리스트 초기화
    rows_to_keep = []
    found_and_deleted = False
    
    # 원본 파일 읽기
    try:
        with open('parking.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == target:
                    # 일치하는 데이터를 찾았으므로 삭제하고 continue
                    found_and_deleted = True
                    continue
                rows_to_keep.append(row)
    except FileNotFoundError:
        print("파일이 존재하지 않습니다.")
        return

    # 변경 사항이 있는 경우, 파일을 업데이트
    if found_and_deleted:
        with open('parking.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(rows_to_keep)
        print(f"'{target}'에 해당하는 데이터가 삭제되었습니다.")
    else:
        print(f"'{target}'에 해당하는 데이터가 파일에 없습니다.")

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
            exit(most_common_text)
            should_continue = False  # 중복 텍스트가 10번 이상 나타나면 반복 종료

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
