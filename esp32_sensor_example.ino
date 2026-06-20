#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

#define DHTPIN 15
#define DHTTYPE DHT22

#define SOIL_PIN 34
#define PUMP_PIN 4

DHT dht(DHTPIN, DHTTYPE);

// WiFi credentials
const char* ssid = "Rishika's Galaxy A13";
const char* password = "ihnk6918";


int soilThreshold = 2200;

void setup() {

  Serial.begin(115200);

  pinMode(PUMP_PIN, OUTPUT);
  digitalWrite(PUMP_PIN, LOW);

  dht.begin();

  Serial.println("Smart Agriculture System Starting...");

  WiFi.begin(ssid, password);

  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi Connected");
}

void loop() {

  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  int soilMoisture = analogRead(SOIL_PIN);

  Serial.println("------------- SENSOR DATA -------------");

  Serial.print("Temperature: ");
  Serial.println(temperature);

  Serial.print("Humidity: ");
  Serial.println(humidity);

  Serial.print("Soil Moisture: ");
  Serial.println(soilMoisture);

  // Pump Control
  if (soilMoisture > soilThreshold) {

    Serial.println("Soil Dry - Pump ON");
    digitalWrite(PUMP_PIN, HIGH);

  } else {

    Serial.println("Soil Wet - Pump OFF");
    digitalWrite(PUMP_PIN, LOW);

  }

  // Send Data to Cloud
  if (WiFi.status() == WL_CONNECTED) {

    HTTPClient http;

  

    if (httpCode > 0) {
      Serial.print("Data sent to ThingSpeak. Response: ");
      Serial.println(httpCode);
    }
    else {
      Serial.println("Error sending data");
    }

    http.end();
  }

  Serial.println("---------------------------------------");

  delay(2000);   // ThingSpeak limit (15 sec)
}