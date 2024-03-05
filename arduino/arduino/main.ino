#include <Servo.h>                                  // Servo 라이브러리 헥사 선언
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);  // I2C 주소와 LCD 화면 크기 설정 (16x2)
Servo myservo;                                        // 서보모터 선언

int pos = 0;                                               // 모터 위치를 확인하기 위해 변수를 선언
int servoPin = 6;                                       // 모터 제어를 위해 6번핀(PWM) 으로 선언

void setup() {
  Serial.begin(9600);
  pinMode (servoPin, OUTPUT);           // 모터 제어핀을 출력으로 설정
  myservo.attach(6);                                // 모터의 신호선을 6번핀에 연결
  delay(2);
  myservo.write(80);

  lcd.init();                      // LCD 초기화
  lcd.backlight();                 // 백라이트 활성화
  lcd.clear();                     // 화면 지우기
}


void gate_open() {
  myservo.write(0);
}

void gate_close(){
  myservo.write(80);
}


void print_lcd(String line1, String line2) {
  lcd.clear();                   // 화면 지우기
  lcd.setCursor(0, 0);          // LCD 커서 위치 설정
  lcd.print(line1);       // LCD에 문자열 출력
  lcd.setCursor(0, 1);          // 다음 줄로 이동
  lcd.print(line2);             // LCD에 입력된 문자열 출력
}

void loop() {
  if (Serial.available() > 0) {
    String c = Serial.readString();

    if (c == "open") {
      gate_open();

      print_lcd("Received", c);

    } 
    else if (c == "close") {
      gate_close();
      lcd.clear();
    }
  }
}