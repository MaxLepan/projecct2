import RPi.GPIO as GPIO
import time
import signal

colors = [0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0xFF00FF, 0x00FFFF]
pins = {'pin_R':29, 'pin_G':31, 'pin_B':33}  # pins is a dict
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(29, GPIO.OUT)# Numbers GPIOs by physical location
for i in pins:
	GPIO.setup(pins[i], GPIO.OUT)   # Set pins' mode is output
	GPIO.output(pins[i], GPIO.HIGH) # Set pins to high(+3.3V) to off led


def map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def setColor(col):   # For example : col = 0x112233
	R_val = (col & 0xFF0000) >> 16
	G_val = (col & 0x00FF00) >> 8
	B_val = (col & 0x0000FF) >> 0
	
	R_val = map(R_val, 0, 255, 0, 100)
	G_val = map(G_val, 0, 255, 0, 100)
	B_val = map(B_val, 0, 255, 0, 100)
	
	p_R.ChangeDutyCycle(R_val)     # Change duty cycle
	p_G.ChangeDutyCycle(G_val)
	p_B.ChangeDutyCycle(B_val)
	
def end_process():
	p_R.stop()
	p_G.stop()
	p_B.stop()
	for i in pins:
		GPIO.output(pins[i], GPIO.HIGH)    # Turn off all leds
	GPIO.cleanup()
GPIO.output(29, GPIO.HIGH)
signal.signal(signal.SIGTERM, end_process)

try:
	while True:
		GPIO.output(29, GPIO.HIGH)
except :
	GPIO.output(29, GPIO.LOW)    # Turn off all leds
	GPIO.cleanup()