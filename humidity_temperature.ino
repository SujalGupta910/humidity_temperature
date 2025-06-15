#include "DHT.h"

#define DHTPIN 2
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  delay(1000); // 1 second interval

  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  if (isnan(humidity) || isnan(temperature)) {
    // Optional: Output error in a different format, or skip
    return;
  }

  // Output in CSV format: humidity,temperature
  Serial.print(humidity, 2);     // 1 decimal place
  Serial.print(",");
  Serial.println(temperature, 2);
}
