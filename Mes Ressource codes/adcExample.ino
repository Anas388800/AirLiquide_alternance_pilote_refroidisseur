uint16_t samplingRate = 1000;
uint32_t isr_count = 0;
uint32_t counter = 0;
bool led = false;

inline void fastDigitalWrite(int pin, boolean val) {
  if (val)g_APinDescription[pin].pPort -> PIO_SODR = g_APinDescription[pin].ulPin;
  else    g_APinDescription[pin].pPort -> PIO_CODR = g_APinDescription[pin].ulPin;
}

void setup() {
  pinMode(LED_BUILTIN, OUTPUT); 		//	define LED pin as output
  digitalWrite(LED_BUILTIN, LOW); 		//	set LED pin to LOW
  Serial.begin (115200); 				// 	for debugging
  while (!Serial); 						//	wait for the Serial port to initialize
  adc_setup();         					// 	setup ADC
  tc_setup();          					// 	setup timer
  //  setup_pio_TIOA0();  				// 	drive Arduino pin 2 at sampleRate to bring clock out
}

void setup_pio_TIOA0() { 				// 	Configure Ard pin 2 as output from TC0 channel A (copy of trigger event)
  PIOB->PIO_PDR = PIO_PB25B_TIOA0;  	// 	disable PIO control
  PIOB->PIO_IDR = PIO_PB25B_TIOA0;   	// 	disable PIO interrupts
  PIOB->PIO_ABSR |= PIO_PB25B_TIOA0;  	// 	switch to B peripheral
}

void adc_setup() {
  NVIC_EnableIRQ (ADC_IRQn);   			// enable ADC interrupt vector
  ADC->ADC_IDR = 0xFFFFFFFF;   			// disable interrupts
  ADC->ADC_IER = 0x1;  					// enable AD0 and AD1 End-Of-Conv interrupt (Arduino pins A7 and A6)
  ADC->ADC_CHDR = 0xFFFF;      			// disable all channels
  ADC->ADC_CHER = 0x1;        			// enable A7 and A6
  ADC->ADC_CGR = 0x55555555;  			// All gains set to x1
  ADC->ADC_COR = 0x00000000;   			// All offsets off

  ADC->ADC_MR = (ADC->ADC_MR & 0xFFFFFFF0) | ADC_MR_TRGSEL_ADC_TRIG1 | ADC_MR_TRGEN;  // 1 = trig source TIO from TC0
}

void tc_setup() {
  pmc_enable_periph_clk (TC_INTERFACE_ID);   // clock the TC0 channel 0

  TcChannel * t = &(TC0->TC_CHANNEL)[0];     // pointer to TC0 registers for its channel 0
  t->TC_CCR = TC_CCR_CLKDIS;  				 // disable internal clocking while setup regs
  t->TC_IDR = 0xFFFFFFFF;     				 // disable interrupts
  t->TC_SR;                   				 // read int status reg to clear pending
  t->TC_CMR = TC_CMR_TCCLKS_TIMER_CLOCK1 |   // use TCLK1 (prescale by 2, = 42MHz)
              TC_CMR_WAVE |                  // waveform mode
              TC_CMR_WAVSEL_UP_RC |          // count-up PWM using RC as threshold
              TC_CMR_EEVT_XC0 |     		 // Set external events from XC0 (this setup TIOB as output)
              TC_CMR_ACPA_CLEAR | TC_CMR_ACPC_CLEAR |
              TC_CMR_BCPB_CLEAR | TC_CMR_BCPC_CLEAR;

  //  t->TC_RC =  875 ;     // counter resets on RC, so sets period in terms of 42MHz clock
  //  t->TC_RA =  440 ;     // roughly square wave

  t->TC_RC = VARIANT_MCK / 2 / (2 * samplingRate); //<*********************  Frequency = (Mck/2)/TC_RC = sampleRate
  t->TC_RA = VARIANT_MCK / 2 / (4 * samplingRate); //<********************   About 50% duty cycle

  t->TC_CMR = (t->TC_CMR & 0xFFF0FFFF) | TC_CMR_ACPA_CLEAR | TC_CMR_ACPC_SET;  // set clear and set from RA and RC compares

  t->TC_CCR = TC_CCR_CLKEN | TC_CCR_SWTRG;  	 // re-enable local clocking and switch to hardware trigger source.
}

void ADC_Handler() {
  volatile uint32_t sr = ADC->ADC_ISR; 			 // read ADC status register
  if (sr & ADC_ISR_EOC0 || sr & ADC_ISR_EOC1) {  // ensure there was an End-of-Conversion and we read the ISR reg
    ++isr_count; 							     // increment the ISR counter
  }
}

void loop() {
  if (isr_count >= samplingRate) { // blink LED every 1 second
    if (led) {
      fastDigitalWrite(LED_BUILTIN, LOW);
      led = false;
    }
    else {
      fastDigitalWrite(LED_BUILTIN, HIGH);
      led = true;
    }
    isr_count = 0; // reset isr counter
  }
}

