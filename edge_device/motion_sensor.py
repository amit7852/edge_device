
import RPi.GPIO as GPIO

PIR_PIN = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

def motion_detected():
    return GPIO.input(PIR_PIN)
