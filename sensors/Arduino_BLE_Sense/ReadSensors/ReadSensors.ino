/*
  HTS221 - Sensor
  - Arduino Nano 33 BLE Sense
*/

#include <Arduino_HTS221.h>

byte comCode;

typedef union {
  float floatingPoint;
  byte binary[4];
} binaryFloat;


void setup() {
  Serial.begin(9600);
  while (!Serial);

  if (!HTS.begin()) {
    Serial.println("Failed to initialize humidity temperature sensor!");
    while (1);
  }
}

void loop() {
  if(Serial.available()){
    // read all the sensor values
    binaryFloat temperature;
    binaryFloat humidity;
    temperature.floatingPoint = HTS.readTemperature();
    humidity.floatingPoint    = HTS.readHumidity();
    
    comCode = Serial.read();
    // we are requested the information
    if(comCode==0x00){
      Serial.write(temperature.binary, 4);
      Serial.write(humidity.binary, 4);
    }
  }
}
