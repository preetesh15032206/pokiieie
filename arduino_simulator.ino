/*
  AI Weather Forecast Simulator
  Simulates atmospheric evolution over 2 hours for training forecasting models.
  Format: temperature,humidity,precipitation,uv_index,pressure
*/

unsigned long startTime;
const unsigned long SECOND = 1000;
const unsigned long MINUTE = 60 * SECOND;

void setup() {
  Serial.begin(9600);
  startTime = millis();
}

void loop() {
  unsigned long elapsed = millis() - startTime;
  float temp, humidity, precipitation, uv, pressure;

  if (elapsed < 30 * MINUTE) {
    // PHASE 1 — Sunny
    temp = 30.0 + random(-5, 6) / 10.0;
    humidity = 45.0 + random(-10, 11) / 10.0;
    precipitation = 0.0;
    uv = 8.0 + random(-2, 3) / 10.0;
    pressure = 1014.0 + random(-2, 3) / 10.0;
  } 
  else if (elapsed < 60 * MINUTE) {
    // PHASE 2 — Cloud build-up
    float progress = (float)(elapsed - 30 * MINUTE) / (30 * MINUTE);
    temp = 30.0 - (progress * 3.0);
    humidity = 45.0 + (progress * 15.0);
    precipitation = 0.0;
    uv = 8.0 - (progress * 4.0);
    pressure = 1014.0 - (progress * 4.0);
  } 
  else if (elapsed < 90 * MINUTE) {
    // PHASE 3 — Pre-rain instability
    float progress = (float)(elapsed - 60 * MINUTE) / (30 * MINUTE);
    temp = 27.0 - (progress * 3.0);
    humidity = 60.0 + (progress * 20.0);
    precipitation = progress * 20.0;
    uv = 4.0 - (progress * 3.5);
    pressure = 1010.0 - (progress * 8.0);
  } 
  else if (elapsed < 120 * MINUTE) {
    // PHASE 4 — Rain starts
    float progress = (float)(elapsed - 90 * MINUTE) / (30 * MINUTE);
    temp = 24.0 - (progress * 2.0);
    humidity = 80.0 + (progress * 15.0);
    precipitation = 70.0 + (progress * 25.0);
    uv = 0.5 - (progress * 0.5);
    pressure = 1002.0 - (progress * 7.0);
  } 
  else {
    // Reset cycle after 120 minutes
    startTime = millis();
    return;
  }

  // Add slight noise
  temp += random(-2, 3) / 10.0;
  humidity += random(-5, 6) / 10.0;
  pressure += random(-1, 2) / 10.0;

  Serial.print(temp); Serial.print(",");
  Serial.print(humidity); Serial.print(",");
  Serial.print(precipitation); Serial.print(",");
  Serial.print(uv); Serial.print(",");
  Serial.println(pressure);

  delay(5000);
}
