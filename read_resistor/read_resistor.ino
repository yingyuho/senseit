int level = 0;
int aread = -1;
const int NUM_JOINTS = 8;
const int d_high[NUM_JOINTS] = {0, 2, 3, 5, 5, 7, 9, 9};
const int d_low[NUM_JOINTS] = {1, 1, 4, 4, 6, 8, 8, 10};
const int a_in[NUM_JOINTS] = {A0, A1, A2, A3, A3, A4, A5, A5};
const int d_map[] = {32, 34, 36, 38, 40, 42, 44, 46, 7, 6, 4};
/*
 * P0 = 32, ..., P7 = 46
 * P8 = 7, P9 = 6, P10 = 4
 */

void setup() {
  // initialize serial:
  Serial.begin(115200);
  //analogReference(INTERNAL1V1);
}

void loop() {
  int data = 0;
  int dh = -1, dl = -1, ai = -1;
  // if there's any serial available, read it:
  while (Serial.available() > 0) {
    data = Serial.parseInt();
    if (Serial.read() != '\n')
      continue;
    if (data >= 0 && data < NUM_JOINTS) {
      dh = d_map[d_high[data]];
      dl = d_map[d_low[data]];
      ai = a_in[data];
      pinMode(dh, OUTPUT);
      pinMode(dl, OUTPUT);
      digitalWrite(dh, HIGH);
      digitalWrite(dl, LOW);
      aread = analogRead(ai);
      Serial.println(aread, DEC);
      pinMode(dh, INPUT);
      pinMode(dl, INPUT);
    }
  }
}


