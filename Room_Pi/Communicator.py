import pika, socket, uuid, json, threading
from zeroconf import *
import time
#!/usr/bin/env python
__author__ = 'jason'

#HOST_IP is currently device ip
#change HOST_IP if current device changed
HOST_IP = '10.0.1.18'

#This class will handle all the communication within the room pi.
#It also need to handle the communication between controller pi and client pi
class Communicator(object):
    def __init__(self, roomID):
        self.Client_Connected = False
        self.Controller_Connected = False
        self.Controller_ip = ''
        self.roomname = roomID
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST_IP))
        self.channel = self.connection.channel()

    def _startService_(self):
        self.desc = {'qname': 'Room1_queue'}
        self.info = ServiceInfo("_http._tcp.local.",
                        "Room_http._tcp.local.",
                       socket.inet_aton(socket.gethostbyname(socket.gethostname())), 80, 0, 0,
                       self.desc, "Room1")

        self.zeroconf = Zeroconf()
        print "Registration of a service, press Ctrl-C to exit..."
        self.zeroconf.register_service(self.info)

    def _removeService_(self):
        #Unregiste service form local network when system Exit.
        print "Unregistering..."
        self.zeroconf.unregister_service(self.info)
        self.zeroconf.close()
        print "Room1 offline"

    #send music player information to Controller, cSong is tra>k name
    def _SendMusicPlayerInfo_(self, track, trackstatus):
        self.MusicInfo = {'sender': 'Room', 'roomID': self.roomname, 'device': 'MusicPlyer', 'Track': track, 'TrackStatus': trackstatus}
        print " [x] Sent 'Music Player information!'"
        self.channel0.basic_publish(exchange='',
                               routing_key='Control_Room_queue',
                               body=json.dumps(self.LED_Status))


    def _SendLEDInfo_(self, ledstatus):
        self.LED_Status = {'sender': 'Room', 'roomID': self.roomname, 'device': 'LED', 'LEDStatus': ledstatus}
        print " [x] Sent 'LED information!'"
        self.channel0.basic_publish(exchange='',
                               routing_key='Control_Room_queue',
                               body=json.dumps(self.LED_Status))

    def _ConnectMQ_(self):
        #connect Room queue to RabbitMQ
        self.channel.queue_declare(queue='Room1_queue')#declare queue name as control_queue
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(on_request, queue='Room1_queue')

    def _ConnectController_(self):
        print "Connect to controller using zeroconfig"
        zeroconf = Zeroconf()
        #if processClientMSG['target'] == 'Room1':
        listener1 = MyListener_Controller()
        binfo1 = listener1.add_service(zeroconf,"_http._tcp.local.","Controller_http._tcp.local.")
        self.Controller_ip = binfo1.bhost
        self.connection0 = pika.BlockingConnection(pika.ConnectionParameters(host=self.Controller_ip))
        self.channel0 = self.connection0.channel()
        self.channel0.queue_declare(queue='Control_Room_queue')


    def _consumingThread_(self):
        t = threading.Thread(target=self.channel.start_consuming)
        t.daemon = True
        t.start()


#zero config for controller pi, this listener is a filter that only return Controller's service information
class MyListener_Controller(object):

    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        print info
        if info is not None:
            print info.get_Server()
            if info.get_Server() == "Controller.":
                bottleinfo = setinfo(str(socket.inet_ntoa(info.get_Address())),info.get_Properties())
                return bottleinfo

#Zero config helper function, will store host address and properties
class setinfo(object):
    def __init__(self,bhost,bproper):
        self.bhost = bhost
        self.bproper = bproper

def on_request(ch, method, props, body):
    n = body

    print "Recive information from Room_Pi: %s"  % (n,)
    response = n

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)
