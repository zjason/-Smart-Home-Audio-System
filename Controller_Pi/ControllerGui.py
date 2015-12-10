#This is a controller GUI Program
import socket, pika, json, uuid, threading
#Uncomment the next line to enable GUI import
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread, QPointF, QTimer
import sys
from PyQt5.QtWidgets import QApplication
#from main_controller import MainController
from zeroconf import *


#--------------------------------------------------------------------------------
HOST_IP = '172.31.174.131'

class ControllerCommunication(QObject):

    led = pyqtSignal(str)

    def __init__(self):
        super(ControllerCommunication, self).__init__()
        self.Room1_Connected = False
        self.Room2_Connected = False
        self.currentRoom = ""
        #self.startControlService()
        self.connectControl_ClientMQ()
        self.connectControl_RoomMQ()
        self.connect_room()

    def startControlService(self):
        #announcing a service to local internet (zero-config)
        desc = {'qname': 'control_queue'}
        self.info = ServiceInfo("_http._tcp.local.",
                       "Controller_http._tcp.local.",
                       socket.inet_aton(socket.gethostbyname(socket.gethostname())), 80, 0, 0,
                       desc, "Controller")

        self.zeroconf = Zeroconf()
        self.zeroconf.register_service(self.info)
        print "Registration of a service, press Ctrl-C to exit..."

    def removeControlService(self):
        #Unregiste service form local network when system Exit.
        print "Unregistering..."
        self.zeroconf.unregister_service(self.info)
        self.zeroconf.close()

    def connect_room(self):
        print "test Room zeroconfig"
        zeroconf = Zeroconf()
        self.room1 = RoomMQ('172.30.39.27')
        self.Room1_Connected = True
        print 'room1 connected:', self.Room1_Connected
        # listener1 = MyListener_Room('Room1')
        # binfo1 = listener1.add_service(zeroconf,"_http._tcp.local.","Room_http._tcp.local.")
        # #connect room1
        # if binfo1 is not None:
        #         # print "Controller host is ", binfo1.bhost
        #         # print "Controller proper is ", binfo1.bproper
        #         #self.room1 = RoomMQ(binfo1.bhost, binfo1.bproper)
        #     self.room1 = RoomMQ(binfo1.bhost)
        #     self.Room1_Connected = True
        #     print 'room1 connected:', self.Room1_Connected
        #         #print 'message received from Room1',self.room1.call(clientmsg)
        # else:
        #     print 'Did not found Room1 pi!'
        #elif processClientMSG['target'] == 'Room2':
        # listener2 = MyListener_Room('Room2')
        # binfo2 = listener2.add_service(zeroconf,"_http._tcp.local.","Room_http._tcp.local.")
        # #connect room2
        # if binfo2 is not None:
        #         # print "Controller host is ", binfo2.bhost
        #         # print "Controller proper is ", binfo2.bproper
        #         #self.room2 = RoomMQ(binfo2.bhost, binfo2.bproper)
        #     self.room2 = RoomMQ(binfo2.bhost)
        #     self.Room2_Connected = True
        #     print 'Room2 connected:', self.Room2_Connected
        #     #print 'message received from Room2',self.room2.call(clientmsg)
        # else:
        #     print 'Did not found Room2 pi!'

    #This function will handle all the message analysis
    def messageHandler(self,message):
        processMSG = json.loads(message)
        if processMSG['sender'] == 'Client':
            print "send message to Room"
            if processMSG['target'] == '':
                print " send to current Room"
                self.room1.call(message)
                return 'already send message to current Room'
                # if self.currentRoom == 'Room1':
                #     self.room1.call(message)
                # elif self.currentRoom == 'Room2':
                #     self.room2.call(message)
            else:
                print " send to target Room"
                if processMSG['target'] == 'Room1':
                    return self.room1.call(message)
                elif processMSG['target'] == 'Room2':
                    return self.room2.call(message)
        elif processMSG['sender'] == 'Room':
            if (processMSG['device'] == 'LED'):
                print "emit a LED signal to GUI"
                if(processMSG['LEDStatus'] == 'ON'):
                    self.currentRoom = 'Room1'
                    self.led.emit(str('ON'))
                else:
                    self.currentRoom = ''
                    self.led.emit(str('OFF'))
            else:
                print "emit a MusicPlayer signal to GUI"
            return "got message form Room"

    def connectControl_ClientMQ(self):
        #connect Controller GUI to RabbitMQ
        self.connection0 = pika.BlockingConnection(pika.ConnectionParameters(host=HOST_IP))
        self.channel0 = self.connection0.channel()
        self.channel0.queue_declare(queue='Control_Client_queue')#declare queue name as control_queue
        self.channel0.basic_qos(prefetch_count=1)
        self.channel0.basic_consume(self.on_request_Client, queue='Control_Client_queue')

    def on_request_Client(self, ch, method, props, body):
        n = body
        response = self.messageHandler(n)
        print "Recive information from Room_Pi: %s"  % (n,)

        ch.basic_publish(exchange='',
                    routing_key=props.reply_to,
                    properties=pika.BasicProperties(correlation_id = \
                                                       props.correlation_id),
                    body=str(response))
        ch.basic_ack(delivery_tag = method.delivery_tag)

    def connectControl_RoomMQ(self):
        #connect Controller GUI to RabbitMQ
        self.connection1 = pika.BlockingConnection(pika.ConnectionParameters(host=HOST_IP))
        self.channel1 = self.connection1.channel()
        self.channel1.queue_declare(queue='Control_Room_queue')#declare queue name as control_queue
        self.channel1.basic_qos(prefetch_count=1)
        self.channel1.basic_consume(self.on_request_Room, queue='Control_Room_queue',no_ack=True)

    def on_request_Room(self,ch, method, props, body):
        n = body
        print self.messageHandler(n)
        print "Recive information from Room_Pi: %s"  % (n,)

    def _consumingThread_(self):
        t0 = threading.Thread(target=self.channel0.start_consuming)
        t0.daemon = True
        t0.start()
        t1 = threading.Thread(target=self.channel1.start_consuming)
        t1.daemon = True
        t1.start()

#zero config for controller pi, this listener is a filter that only return Controller's service information
class MyListener_Room(object):
    def __init__(self, servicename):
        self.serviceID = servicename

    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        if info is not None:
            #print info.get_Server()
            if info.get_Server() == self.serviceID+".":
                bottleinfo = Setinfo(str(socket.inet_ntoa(info.get_Address())),info.get_Properties())
                return bottleinfo

#Zero config helper function, will store host address and properties
class Setinfo(object):
    def __init__(self,bhost,bproper):
        self.bhost = bhost
        self.bproper = bproper

#Controller pi RabbitMQ sender
class RoomMQ(object):
    def __init__(self,chost):
        self.Room_host = chost
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=self.Room_host))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='Room1_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=n)
        while self.response is None:
            self.connection.process_data_events()
        return self.response



# def on_request_Room(ch, method, props, body):
#     n = body
#     print ControllerCommunication.messageHandler(n)
#     print "Recive information from Room_Pi: %s"  % (n,)

#--------------------------------------------------------------------------------

#
# try:
#     #create a controllerCommunication instance to send client message to Room
#     #test = ControllerCommunication()
#     test._consumingThread_()
#
# except SystemExit:
#     #Unregiste service form local network when system Exit.
#     test.removeControlService()



