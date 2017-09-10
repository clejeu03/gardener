# Read values from the ADS1x115 and print them on the screen
import time

# Import the ADS1x15 module.
import Adafruit_ADS1x15

# To control the LED, we import the GPIO library
import RPi.GPIO as GPIO

def SetupLeds(*leds):
   GPIO.cleanup()
   GPIO.setmode(GPIO.BCM)
   for led in leds:
       GPIO.setup(led, GPIO.OUT)
       GPIO.output(led, GPIO.LOW)

def Blink(*leds):
   for led in leds:
	GPIO.output(led, GPIO.HIGH)
	time.sleep(1)
	GPIO.output(led, GPIO.LOW)   

def PrintMoistureValues():
   # ADS1x115 has 4 input channels but we are only reading the Channel 0 and 1
   print('Reading ADS1x15 values for Channel 0 and 1, press Ctrl-C to quit...')
   print('| {0:>6} | {1:>6} |'.format(*range(2)))
   print('-'*17)   

   # Main loop.
   while True:
   	# Read all the ADC channel values in a list.
	values = [0]*2
	for i in range(2):
		# Raw value is encoded on 16 bits (ADS1x115) so it belongs to the range (-32768,32767). 
		# To read the voltage, we take as a reference that value 32767 is equivalent to 4,096V as described on ADS1x115 datasheet
		values[i] = ( adc.read_adc(i, gain=GAIN) *4.096)/32767
	print('| {0:.4f} | {1:.4f} |'.format(*values))
	# Pause for half a second.
	time.sleep(0.5)

def LightUpWhenDry(*leds):
	# Read all the ADC channel values in a list.
	values = [0]*2
	for i in range(2):
		# Raw value is encoded on 16 bits (ADS1x115) so it belongs to the range (-32768,32767). 
		# To read the voltage, we take as a reference that value 32767 is equivalent to 4,096V as described on ADS1x115 datasheet
		values[i] = ( adc.read_adc(i, gain=GAIN) *4.096)/32767
	
        # If any plant is too dry, light the LED 
	if values[0] > DRY or values[1] > DRY:
		print('Dry')
		Blink(leds)
	else:
		print('wet')

	# Pause for half a second.
	time.sleep(0.5)
   
if __name__=='__main__':
    # Create an ADS1115 ADC (16-bit) instance.
    adc = Adafruit_ADS1x15.ADS1115()

    # Choose a gain of 1 for reading voltages from 0 to 4.09V.
    # Or pick a different gain to change the range of voltages that are read:
    #  - 2/3 = +/-6.144V
    #  -   1 = +/-4.096V
    #  -   2 = +/-2.048V
    #  -   4 = +/-1.024V
    #  -   8 = +/-0.512V
    #  -  16 = +/-0.256V
    # See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
    GAIN = 1

    #Define LED GPIO number here
    LED = 18

    # Define Moisture Sensor channels on the ADC
    PLANTE_0 = 0
    PLANTE_1 = 1

    # Define the moisture Thresholds in percentage
    WET = 2.00 # Voltage superior to that value stops pump (?)
    DRY = 3.00 # Voltage inferior to that value triggers pump

    # Setup the LEDs
    SetupLeds(LED)

    # Main loop
    try : 
	while True:
		LightUpWhenDry(LED)	

    # stop on Ctrl+C and clean up
    except KeyboardInterrupt:
	GPIO.cleanup()
    
