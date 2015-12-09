#This is a controller GUI Program
import socket, pika, json, uuid, threading
#Uncomment the next line to enable GUI import
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread, QPointF, QTimer
from zeroconf import *
import sys
from PyQt5.QtWidgets import QApplication
from main_controller import MainController


#--------------------------------------------------------------------------------
#change HOST_IP to current device IP
HOST_IP = '172.31.174.131'

led = pyqtSignal()

class ControllerCommunication(QObject):


    def __init__(self):
        super(ControllerCommunication, self).__init__()
        self.Room1_Connected = False
        self.Room2_Connected = False
        self.currentRoom = ""
        self.connect_room()

    def connect_room(self):
        print "test Room zeroconfig"
        zeroconf = Zeroconf()
        #if processClientMSG['target'] == 'Room1':
        listener1 = MyListener_Room('Room1')
        binfo1 = listener1.add_service(zeroconf,"_http._tcp.local.","Room_http._tcp.local.")
        #connect room1
        if binfo1 is not None:
                # print "Controller host is ", binfo1.bhost
                # print "Controller proper is ", binfo1.bproper
                #self.room1 = RoomMQ(binfo1.bhost, binfo1.bproper)
            self.room1 = RoomMQ(binfo1.bhost)
            self.Room1_Connected = True
            print 'room1 connected:', self.Room1_Connected
                #print 'message received from Room1',self.room1.call(clientmsg)
        else:
            print 'Did not found Room1 pi!'
        #elif processClientMSG['target'] == 'Room2':
        listener2 = MyListener_Room('Room2')
        binfo2 = listener2.add_service(zeroconf,"_http._tcp.local.","Room_http._tcp.local.")
        #connect room2
        if binfo2 is not None:
                # print "Controller host is ", binfo2.bhost
                # print "Controller proper is ", binfo2.bproper
                #self.room2 = RoomMQ(binfo2.bhost, binfo2.bproper)
            self.room2 = RoomMQ(binfo2.bhost)
            self.Room2_Connected = True
            print 'Room2 connected:', self.Room2_Connected
            #print 'message received from Room2',self.room2.call(clientmsg)
        else:
            print 'Did not found Room2 pi!'


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

#--------------------------------------------------------------------------------
#This function will handle all the message analysis
def messageHandler(message):
    processMSG = json.loads(message)
    if processMSG['sender'] == 'Client':
        print "send message to Room"
        if processMSG['target'] == '':
            print " send to current Room"
        else:
            print " send to target Room"
            if processMSG['target'] == 'Room1':
                return test.room1.call(message)
            elif processMSG['target'] == 'Room2':
                return test.room2.call(message)
    elif processMSG['sender'] == 'Room':
        led.emit()
        print "emit a signal to GUI"
        return "got message form Room"


#--------------------------------------------------------------------------------
#connect Controller GUI to RabbitMQ
connection0 = pika.BlockingConnection(pika.ConnectionParameters(host=HOST_IP))
channel0 = connection0.channel()
channel0.queue_declare(queue='Control_Client_queue')#declare queue name as control_queue

def on_request(ch, method, props, body):
    n = body
    response = messageHandler(n)

    print "Recive information from Room_Pi: %s"  % (n,)

    ch.basic_publish(exchange='',
                    routing_key=props.reply_to,
                    properties=pika.BasicProperties(correlation_id = \
                                                       props.correlation_id),
                    body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel0.basic_qos(prefetch_count=1)
channel0.basic_consume(on_request, queue='Control_Client_queue')

#--------------------------------------------------------------------------------
#connect Controller GUI to RabbitMQ
connection1 = pika.BlockingConnection(pika.ConnectionParameters(host=HOST_IP))
channel1 = connection1.channel()
channel1.queue_declare(queue='Control_Room_queue')#declare queue name as control_queue

def on_request(ch, method, props, body):
    n = body
    #response = messageHandler(n)
    print "Recive information from Room_Pi: %s"  % (n,)

    #print "no reply queue", response


channel1.basic_qos(prefetch_count=1)
channel1.basic_consume(on_request, queue='Control_Room_queue',no_ack=True)
#--------------------------------------------------------------------------------

# Make a instence of the mainwindow class
# win = MainWindow()
# win.connect("delete-event", Gtk.main_quit)
# win.show_all()

if __name__ == '__main__':

    try:
    #announcing a service to local internet (zero-config)
        desc = {'qname': 'control_queue'}
        info = ServiceInfo("_http._tcp.local.",
                       "Controller_http._tcp.local.",
                       socket.inet_aton(socket.gethostbyname(socket.gethostname())), 80, 0, 0,
                       desc, "Controller")

        zeroconf = Zeroconf()
        print "Registration of a service, press Ctrl-C to exit..."
        zeroconf.register_service(info)
    #create a controllerCommunication instance to send client message to Room
        test = ControllerCommunication()
    # start consuming message from control_queue
        print 'start thread1'
    #channel0.start_consuming
        t0 = threading.Thread(target=channel0.start_consuming)
        t0.daemon = True
        t0.start()
        print 'did not block'
        t1 = threading.Thread(target=channel1.start_consuming)
        t1.daemon = True
        t1.start()
        # channel1.start_consuming()
        a = QApplication(sys.argv)
        w = MainController()
        w.start()
        sys.exit(a.exec_())
    except SystemExit:
    #Unregiste service form local network when system Exit.
        print "Unregistering..."
        zeroconf.unregister_service(info)
        zeroconf.close()

