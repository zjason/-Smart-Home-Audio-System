#!/usr/bin/python

from VCNL4000 import VCNL4000
import time
import threading

class Detector(object):
    """
    sensor detector base class, update led
    status according to the sensor reading
    @:param
    """
    # Constructor
    # initiating sensor and reading thread
    def __init__(self):
        self.LED = False
        self.vcnl = VCNL4000(0x13)
        t = threading.Thread(target=self.check_present)
        t.daemon = True
        t.start()

    # check proximity
    def check_present(self):
        while True:
            if self.vcnl.read_proximity() > 10000:
                print "Present !!!!"
                self.LED = True
                time.sleep(0.1)
            else:
                print "No one"
                self.LED = False
                time.sleep(0.1)

    def check_led(self):
        return self.LED

try:
    detctor = Detector()
    while 1:
        time.sleep(2)
        print("LED status:"), detctor.check_led()

except (KeyboardInterrupt):
    print "sensor closed"


