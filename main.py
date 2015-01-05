import json
import RPi.GPIO as GPIO
import time
from datetime import timedelta
from datetime import datetime

done_time = 4

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN) # Piezzo for Dryer
GPIO.setup(12, GPIO.OUT)# Status LED
GPIO.setup(15, GPIO.IN) # Switch for Turning off Input

# keep two time stamps for deciding when to notify
start_event = None
now_event = datetime.now()

while True:
    if GPIO.input(15):
        GPIO.output(12, GPIO.HIGH)
        if start_event == None:
            start_event = datetime.now()
            print ("START %s now %s" % (start_event, now_event)) 
        if GPIO.input(11):
            now_event = datetime.now()
            print ("start %s NOW %s" % (start_event, now_event)) 

        if (now_event - start_event).total_seconds() >= done_time:
            start_event = None
            GPIO.output(12, GPIO.LOW)
            print("done")
            exit()
        time.sleep(1)

    else:
        GPIO.output(12, GPIO.LOW)
        print ("Not running.")
        time.sleep(5)
            
GPIO.cleanup()
