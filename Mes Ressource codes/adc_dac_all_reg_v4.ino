// identifies that microcontroller for the Arduino Due
#define __SAM3X8E__

// Stores data value read from ADC
int analog_data;

void setup(void) {    
  ADC->ADC_MR = 0x00000000 ; // ADC full speed
  ADC->ADC_IDR = 0xFFFFFFFF ; // disable ADC interrupts
  
  ADC->ADC_CHER = 0x00000001 << 7 ; // enable the ADC, just ch0
  
  pmc_enable_periph_clk (DACC_INTERFACE_ID) ; // start clocking DACC

  DACC->DACC_IDR = 0xFFFFFFFF ; // no interrupts
  DACC->DACC_CHER = 0x00000001 ; // enable DACC chan0
}

void loop(void) {
    // start first ADC conversion
    ADC->ADC_CR = 0x00000002 ;
   
    // Read the value from ADC last conversion data register.
    analog_data = ADC->ADC_LCDR & 0x00000FFF ;

    // Write the value just read to the DACC conversion data register.
    DACC->DACC_CDR = analog_data ;
}
 

