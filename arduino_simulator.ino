/*
  Atmospheric AI Forecast Engine - Simulator
  Simulates atmospheric evolution over 120 minutes with pressure dynamics.
  Format: temperature,humidity,precipitation,uv_index,pressure
*/

unsigned long startTime;
const unsigned long SECOND = 1000;
const unsigned long MINUTE = 60 * SECOND;

void setup() {
  Serial.begin(9600);
  startTime = millis();
  randomSeed(analogRead(0));
}

void loop() {
  unsigned long elapsed = (millis() - startTime) % (120 * MINUTE);
  float temp, humidity, precipitation, uv, pressure;

  if (elapsed < 30 * MINUTE) {
    // PHASE 1 – Stable Sunny Atmosphere
    temp = 31.0 + random(-10, 11) / 10.0;
    humidity = 45.0 + random(-50, 51) / 10.0;
    precipitation = 0.0;
    uv = 8.0 + random(-10, 11) / 10.0;
    pressure = 1014.5 + random(-15, 16) / 10.0;
  } 
  else if (elapsed < 60 * MINUTE) {
    // PHASE 2 – Atmospheric Instability
    float progress = (float)(elapsed - 30 * MINUTE) / (30 * MINUTE);
    temp = 31.0 - (progress * 2.0);
    humidity = 45.0 + (progress * 15.0);
    precipitation = 0.0;
    uv = 8.0 - (progress * 3.0);
    pressure = 1014.5 - (progress * 2.0);
  } 
  else if (elapsed < 90 * MINUTE) {
    // PHASE 3 – Pre-Rain Pressure Drop
    float progress = (float)(elapsed - 60 * MINUTE) / (30 * MINUTE);
    temp = 29.0 - (progress * 4.0);
    humidity = 60.0 + (progress * 15.0);
    precipitation = progress * 15.0;
    uv = 5.0 - (progress * 4.5);
    pressure = 1012.5 - (progress * 6.0);
  } 
  else {
    // PHASE 4 – Rain Event
    float progress = (float)(elapsed - 90 * MINUTE) / (30 * MINUTE);
    temp = 25.0 - (progress * 2.0);
    humidity = 75.0 + (progress * 20.0);
    precipitation = 70.0 + (progress * 20.0);
    uv = 0.5 - (progress * 0.5);
    pressure = 1006.5 - (progress * 8.0);
  }

  // Add micro-variations
  temp += random(-2, 3) / 10.0;
  humidity += random(-5, 6) / 10.0;
  pressure += random(-2, 3) / 10.0;

  Serial.print(temp, 1); Serial.print(",");
  Serial.print(humidity, 1); Serial.print(",");
  Serial.print(precipitation, 1); Serial.print(",");
  Serial.print(uv, 1); Serial.print(",");
  Serial.println(pressure, 1);

  delay(5000);
}
