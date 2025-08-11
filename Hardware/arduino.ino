const int laserPin = 9;
const int sensorPin = A0;
int currentState = 0;

void setup() {
  Serial.begin(9600);
  pinMode(laserPin, OUTPUT);
  digitalWrite(laserPin, LOW);
}

void loop() {
  int sensorValue = analogRead(sensorPin);
  Serial.print(sensorValue);
  Serial.print(",");
  Serial.println(currentState);

  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == '1') {
      digitalWrite(laserPin, HIGH);
      currentState = 1;
    } 
    else if (command == '0') {
      digitalWrite(laserPin, LOW);
      currentState = 0;
    }
  }
  delay(10);
}