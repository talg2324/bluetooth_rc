#include "BluetoothSerial.h" //Header File for Serial Bluetooth, will be added by default into Arduino
#include "Arduino.h"

BluetoothSerial ESP_BT; //Object for Bluetooth

int incoming;
String directions[4] = {"Up","Down","Right", "Left"};
int rightOut = 25;
int leftOut = 22;
int prev = 0;

String comprehend(int bluetooth_signal){
  return directions[bluetooth_signal - 51];
}

void process(int ti, int t){
  double rightVolts = 0;
  double leftVolts = 0;
  Serial.println(ti);
  Serial.println(t);
  if (ti == t){
    if (t == 51){
      Serial.println("5V R, 5V L");
      rightVolts = 255;
      leftVolts = 255;
    }
    else if (t == 53){
      Serial.println("5V R");
      rightVolts = 255;
    }
    else if (t == 54){
      Serial.println("5V L");
      leftVolts = 255;
    }
  }
  else{
    if (t + ti == 104){
      Serial.println("2.5V R, 5V L");
      rightVolts = 126;
      leftVolts = 255;
    }
    else if (t + ti == 105){
      Serial.println("5V R, 2.5V L");
      rightVolts = 255;
      leftVolts = 126;
    }
    else{
      Serial.println("0V output");
    }
  }
  ledcWrite(1, rightVolts);
  ledcWrite(2, leftVolts);
  // dacWrite(25,rightVolts);
}

void setup() {
  
  ledcAttachPin(rightOut, 1); //Initialize output pins
  ledcAttachPin(leftOut, 2);
  
  ledcSetup(1, 0.000005, 8); // 12 kHz PWM, 8-bit resolution
  ledcSetup(2, 0.000005, 8);
  
  Serial.begin(115200); //Start Serial monitor in 115200
  ESP_BT.begin("ESP32"); //Name of your Bluetooth Signal
  Serial.println("Bluetooth Device is Ready to Pair");

}

void loop() {
  
  if (ESP_BT.available()) //Check if we receive anything from Bluetooth
  {
    incoming = ESP_BT.read(); //Read what we receive 
    Serial.print("Received:"); Serial.println(comprehend(incoming));
    if (comprehend(incoming) == "Down"){
      incoming = 0;
    }
    process(prev,incoming);
    prev = incoming;
  }
  delay(5);
}
