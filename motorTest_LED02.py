# Test motor driver with 4 LED's to represent two motors
# forward and reverse.

# By Keith Ellis

# Original version required input from terminal as an input command

# Rev 01 - 03/01/2014
# Trying input from terminal stdin without haveing to press return
# Rev 02 - 07/01/2014
# Impliment PWM so that turning is slower and speeed is incremential
# Impliment drive_motor() function, this receives ducty cycle and pins to 
# set high to drive motors in desired direction




import RPi.GPIO as GPIO
import time
import sys,tty,termios

# 	GPIO output pins in pairs are
#	Left motor, pins 23 & 7
#	Right motor, pins 24 & 8

# 	Setup GPIO output pins
 
gpio_pins = {'leftMotorPin1' : 23, 'leftMotorPin2' : 7, 'rightMotorPin1' : 24,'rightMotorPin2' : 8}

GPIO.setmode(GPIO.BCM)			# Use BCM pin numbers


# Setup all GPIO pins for output

for number in gpio_pins:
	GPIO.setup(gpio_pins[number], GPIO.OUT)
	

''' Setup PWM on all pins '''
frequency = 150

lm1 = GPIO.PWM(gpio_pins['leftMotorPin1'], frequency)	
lm2 = GPIO.PWM(gpio_pins['leftMotorPin2'], frequency)	
rm1 = GPIO.PWM(gpio_pins['rightMotorPin1'], frequency)	
rm2 = GPIO.PWM(gpio_pins['rightMotorPin2'], frequency)


# List to hold PWM variables
pwm=[lm1, lm2, rm1, rm2]

# Start PWM on all four pins
for pin in pwm:
	pin.start(0)


# The getch method can determine which key has been pressed
# by the user on the keyboard by accessing the system files
# It will then return the pressed key as a variable

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


# Stop Function - Sets duty cycle of all pins to zero and sleeps for 0.5 seconds
def stop():
	for pin in pwm:
		pin.ChangeDutyCycle(0)
	time.sleep(0.5)


# drive_motor fuinction, this takes dc (duty cycle or speed from 0 to 100)
# and motors, this is a LIST detailing which GPIO pins should be set to high
# [0,1,2,3] list of pwm
# 0 = left motor forward, 1 = left motor revers, 2 = right motor forward
# 3 = right motor reverse.

def drive_motor(dc,motors):
	stop()
	for n in range(0,dc+1):
		for pin in motors:
			pwm[pin].ChangeDutyCycle(n)
			time.sleep(0.01)


# Main programm - First call stop() to ensure all pins are Low

stop()

# Print control keys to screen as instructions to user

print ("Program Running, use the following keys to control")
print ("1 = Quit \nq = forward\na = reverse\nz = stop\n")
print ("\nu = slow left\n[ = slow right")
print ("o = fast left\np = fast right")


# Get commands from user and send instructions to drive_motor() function

while True:
	n = getch()
	n = n.lower()

	if n == "q":		# Forwards
		drive_motor(100,[0,2])

	elif n == "a":		# Reverse
		drive_motor(100,[1,3])

	elif n == "o":		# fast Left
		drive_motor(80,[1,2])

	elif n == "p":		# fast Right
		drive_motor(80,[0,3])

	elif n == "z":		# stop
		stop()

	elif n == "i":		# slow Left
		drive_motor(80,[2])

	elif n == "[":		# slow Right
		drive_motor(80,[0])

	elif n == "1": 
		print ("Program Ended")
		break
	n=""

GPIO.cleanup()

