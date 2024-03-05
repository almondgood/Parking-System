import cv2
from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
import numpy as np

ocr = PaddleOCR(use_angle_cls=True, lang="korean") 

# web cam
cap = cv2.VideoCapture(0)

while True:
    # 프레임별로 캡처
    ret, frame = cap.read()
    if not ret:
        break

    # PaddleOCR로부터 텍스트 및 바운딩 박스 정보 추출
    result = ocr.ocr(frame, cls=True)
    texts=[]
    # 결과가 None이 아니고, 내용이 있는지 확인
    if result is not None and len(result) > 0:
        # 추출된 정보로부터 바운딩 박스 그리기
        for line in result:
            if line is not None:  # Line이 None이 아닌지 확인
                for info in line:
                    bbox = info[0]  # 바운딩 박스 좌표
                    text = info[1][0]  # 인식된 텍스트
                    confidence = info[1][1]  # 신뢰도
                    if confidence > 0.5:  # 신뢰도가 0.5 이상인 경우에만 그림
                        cv2.rectangle(frame, (int(bbox[0][0]), int(bbox[0][1])), (int(bbox[2][0]), int(bbox[2][1])), (0, 255, 0), 2)
                        # 인식된 텍스트 출력
                        #print(f"Detected Text: {text}, Confidence: {confidence}")
                        texts.append(text)
    print(texts)


    # 수정된 프레임을 화면에 표시
    cv2.imshow('frame', frame)

    # 'q'를 누르면 루프 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 캡처 종료
cap.release()
cv2.destroyAllWindows()
