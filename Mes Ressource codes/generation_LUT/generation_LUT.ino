
const int f = 57;  
const int Fs = 10000 ;                              // sample rate (Hz)
const int LUT_SIZE = 1024 ;                         // lookup table size
int16_t LUT[LUT_SIZE];                              // our sine wave LUT
const int BUFF_SIZE = 175;                // size of output buffer (samples)
int16_t buff[BUFF_SIZE];                            // output buffer
                              // frequency we want to generate (Hz)
const float delta_phi = (float) f / Fs * LUT_SIZE; // phase increment                       
float phase = 0.0f; 
void setup() {

                               // phase accumulator

for (int i = 0; i < LUT_SIZE; ++i)
{
    LUT[i] = (int16_t)roundf(32767 * sinf(2.0f * M_PI * (float)i / LUT_SIZE));
} 

 

// generate buffer of output
for (int i = 0; i < BUFF_SIZE; ++i)
{
    int phase_i = (int)phase;        // get integer part of our phase
    buff[i] = LUT[phase_i];          // get sample value from LUT
    phase += delta_phi;              // increment phase
    if (phase >= (float)LUT_SIZE)    // handle wraparound
        phase -= (float)LUT_SIZE;
}
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.begin(115200);
  for (int i = 0; i < BUFF_SIZE; ++i){
    Serial.println(buff[i]);
  }

}
