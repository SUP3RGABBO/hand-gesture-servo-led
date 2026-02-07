#include <Servo.h>

int LedPin = 3;
int servoPin = 6;

Servo myServo;

void setup() {
  pinMode(LedPin, OUTPUT);   
  myServo.attach(servoPin);
  Serial.begin(9600);       
}

void loop() {
  
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');  

    
    command.trim();

    
    bool isNumber = true;
    for (int i = 0; i < command.length(); i++) {
      if (!isDigit(command[i])) { 
        isNumber = false;
        break;
      }
    }

    if (isNumber) {
      int angle = command.toInt();       
      if (angle < 0) angle = 0;          
      if (angle > 180) angle = 180;
      myServo.write(angle);              
    } else {
     
      if (command == "HIGH") {
        digitalWrite(LedPin, HIGH);
      } else if (command == "LOW") {
        digitalWrite(LedPin, LOW);
      }
    }
  }
}
