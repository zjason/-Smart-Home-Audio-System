from Communicator import *
from test_VCNL4000 import *

#main function, currently for test purpose
def main():
    try:
        communicate = Communicator('Room1')
        communicate._startService_()
        communicate._ConnectMQ_()
        #waite 12 second for Controller GUI start
        time.sleep(5)
        communicate._ConnectController_()
        communicate._consumingThread_()
        sensor = Detector()
        sensorTemp = sensor.check_led()
        while 1:
            time.sleep(1)
            if sensor.check_led() != sensorTemp:
                sensorTemp = sensor.check_led()
                if sensor.check_led() == True:
                    communicate._SendLEDInfo_('ON')
                else:
                    communicate._SendLEDInfo_('OFF')
    except (KeyboardInterrupt, SystemExit):
        communicate._removeService_()


if __name__ == "__main__":
    main()