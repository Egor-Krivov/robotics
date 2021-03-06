#include <math.h>
#include <Servo.h>

// Analog
const int x_pin = 1, y_pin = 0;
// PWM
const int servo1_pin = 10, servo2_pin = 9;

// Control inertia
double moment = 0.9;

double hand1_length = 0.5, hand2_length = 0.5;

const double pi = 3.14;

double x_avg = 0, y_avg = 0;
double theta1 = 0, theta2 = 0;

double ewma(double x, double x_avg) {
  return x_avg * moment + x * (1 - moment);
}


Servo servo1;
Servo servo2;

void setup() {
  servo1.attach(servo1_pin);
  servo2.attach(servo2_pin);

  Serial.begin(9600);
}

void loop() {
  // Something with muliplexor, need to read values twice so that ADC would change port. Maybe fix with delay
  analogRead(x_pin);
  x_avg = ewma(analogRead(x_pin), x_avg);
  analogRead(y_pin);
  y_avg = ewma(analogRead(y_pin), y_avg);
  // Now x and y are in [0, 1023]. Convert them to the right coordinate system here

  // Serial.print(String(x_avg) + " " + String(y_avg) + "\n");
  //TODO convert
  double x = (x_avg - 488) / 512;
  double y = (y_avg - 482) / 512;

  double R = sqrt(sq(x) + sq(y));
  if (R > 1) {
    x /= R;
    y /= R; 
  }
  
  // Compute angles
  double c2 = (sq(x) + sq(y) - sq(hand1_length) - sq(hand2_length)) / (2 * hand1_length * hand2_length);
  double s2 = sqrt(1 - sq(c2));  /// +/-

  double c1 = ((hand1_length + hand2_length * c2) * x + hand2_length * y * s2) / (sq(x) + sq(y));
  double s1 = sqrt(1 - sq(c1));  // +/-

  double theta2 = 180 * atan2(s2, c2) / pi;
  double theta1 = 180 * atan2(s1, c1) / pi;

  Serial.print(String(x) + " " + String(y) + " " + String(theta1) + " " + String(theta2) + "\n");

  // Write
  if (theta1 >=0 & theta2 >= 0) {
    servo1.write(theta1);
    servo2.write(theta2);
  }
}
