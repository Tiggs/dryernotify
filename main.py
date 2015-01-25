import json
import RPi.GPIO as GPIO
import time
import signal
import sys
import json
import urllib2
from datetime import timedelta
from datetime import datetime

done_time = 20
end_point = "http://0.0.0.0:8080/dryer"

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN) # Piezzo for Dryer
GPIO.setup(12, GPIO.OUT)# Switch LED
GPIO.setup(16, GPIO.OUT)# "active" led
GPIO.setup(15, GPIO.IN) # Switch for Turning off Input

# keep two time stamps for deciding when to notify
start_event = None
last_event = None
now_event = datetime.now()

def send_status(status, dt):
    pl = json.dumps({"status": status})
    print ("%s - sending %s" % (dt, status))
    req = urllib2.Request(end_point)
    req.add_header('Content-Type', 'application/json')
    res = urllib2.urlopen(req, pl)
    return res


GPIO.output(16, GPIO.LOW)
while True:
    try:
        if GPIO.input(15):
            # turn on the led status indicator
            GPIO.output(12, GPIO.HIGH)

            if start_event == None:
                start_event = datetime.now()

            if GPIO.input(11):
                if last_event == None:
                   # turn on the first time
                    print ("starting")
                    GPIO.output(16, GPIO.HIGH)
                    send_status("on", start_event)
                    last_event = datetime.now()
                else:
                    last_event = now_event

            now_event = datetime.now()

            if last_event:
                print ("now %s - last %s" % (now_event, last_event))
                if (now_event - last_event).total_seconds() >= done_time:
                    start_event = None
                    last_event = None
                    GPIO.output(16, GPIO.LOW)
                    send_status("off", now_event)
                    time.sleep(done_time)

            time.sleep(1)
        else:
            GPIO.output(12, GPIO.LOW)
            print ("Not running.")
            time.sleep(5)
    except KeyboardInterrupt:
        print ("terminating cleanly")
        send_status("off", datetime.now())
        GPIO.cleanup()
        exit(0)
