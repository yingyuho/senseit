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
 
unsigned long prev_time = 0;
const unsigned long INTV = 1250;
int a_data[NUM_JOINTS];
int n_joint = 0;

void setup() {
  // initialize serial:
  Serial.begin(115200);
  //analogReference(INTERNAL1V1);
}

void loop() {
  unsigned long time = 0;
  int short_data = 0;
  int dh = -1, dl = -1, ai = -1;
  time = micros();
  if (time - prev_time >= INTV) {
    prev_time = time;
    
    dh = d_map[d_high[n_joint]];
    dl = d_map[d_low[n_joint]];
    ai = a_in[n_joint];
    pinMode(dh, OUTPUT);
    pinMode(dl, OUTPUT);
    digitalWrite(dh, HIGH);
    digitalWrite(dl, LOW);
    a_data[n_joint] = analogRead(ai);
    pinMode(dh, INPUT);
    pinMode(dl, INPUT);
    
    n_joint = (n_joint + 1) % NUM_JOINTS;
    if (n_joint == 0) {
        Serial.print("\xff\xff\xff\xff");
        Serial.print("res8");
        for (int i = 0; i < NUM_JOINTS; ++i) {
          short_data = a_data[i];
          Serial.write(short_data & 255);
          short_data >>= 8;
          Serial.write(short_data & 255);
        }
    }
  }
}


