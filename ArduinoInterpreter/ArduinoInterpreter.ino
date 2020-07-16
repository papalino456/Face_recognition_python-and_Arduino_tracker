#include<Servo.h>

Servo serX;
Servo serY;

String tempModify;

void setup() {

  serX.attach(10);
  serY.attach(11);
  Serial.begin(9600);
  Serial.setTimeout(10);
  serX.write(0);
  serY.write(0);
}

void loop() {
  //nothing here
}

void serialEvent() {
tempModify = Serial.readString();

serX.write(parseDataX(tempModify));
serY.write(parseDataY(tempModify));

}

int parseDataX(String data){
  data.remove(data.indexOf("Y"));
  data.remove(data.indexOf("X"), 1);

  return data.toInt();
}

int parseDataY(String data){
  data.remove(0,data.indexOf("Y") + 1);

  return data.toInt();
  
}
