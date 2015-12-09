from Communicator import *

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
        time.sleep(10)
        communicate._SendLEDInfo_('OFF')
        time.sleep(20)
    except (KeyboardInterrupt, SystemExit):
        communicate._removeService_()


if __name__ == "__main__":
    main()