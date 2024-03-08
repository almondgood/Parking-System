import csv
import time

'''
주차요금 1분에 1000원

'''


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
    else:
        print("중복된 데이터가 있습니다. 저장하지 않습니다.")

def entry(car_num):
    timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
    print("Timestamp:", timestamp_str)

    target_vehicle = car_num
    
    check_duplicate_and_save(target_vehicle, timestamp_str)


def exit(target):
    # 임시 리스트 초기화
    rows_to_keep = []
    found_and_deleted = False
    
    # 원본 파일 읽기
    try:
        with open('example.csv', 'r', newline='', encoding='utf-8') as file:
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
        with open('example.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(rows_to_keep)
        print(f"'{target}'에 해당하는 데이터가 삭제되었습니다.")
    else:
        print(f"'{target}'에 해당하는 데이터가 파일에 없습니다.")


# 추가
entry("23가5478")

# 제거
#exit("23가5478")