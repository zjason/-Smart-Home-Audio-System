from Communicator import *
from test_VCNL4000 import *
from music_player import *
import threading

#main function, currently for test purpose
# def main():
#     def checkandsendLED():
#         while 1:
#             time.sleep(1)
#             if sensor.check_led() != sensorTemp:
#                 sensorTemp = sensor.check_led()
#                 if sensor.check_led() == True:
#                     communicate._SendLEDInfo_('ON')
#                 else:
#                     communicate._SendLEDInfo_('OFF')
def main():
    try:
        sensor = Detector()
        mplayer = music_player()
        communicate = Communicator('Room1',sensor, mplayer)
        # communicate._startService_()
        communicate._ConnectMQ_()
        communicate._ConnectController_()
        communicate._consumingThread_()
        sensorTemp = sensor.check_led()
        while 1:
            time.sleep(1)
            print 'check led:', sensor.check_led(), '  led temp', sensorTemp
            if sensor.check_led() != sensorTemp:
                sensorTemp = sensor.check_led()
                if sensor.check_led() == True:
                    communicate._SendLEDInfo_('ON')
                else:
                    communicate._SendLEDInfo_('OFF')
        #threading.Thread(target=checkandsendLED)

    except (KeyboardInterrupt, SystemExit):
        print 'Central Control is offline....'
        #communicate._removeService_()


if __name__ == "__main__":
    main()