#This is a controller GUI Program
import socket, pika, json, uuid, threading
#Uncomment the next line to enable GUI import
#from gi.repository import Gtk
from zeroconf import *


# class MainWindow(Gtk.Window):
#
#     def __init__(self):
#         """
#         constructor, generates the base layout of the central control unit
#         :return:
#         """
#         #Set the window size and border and list box layout
#         Gtk.Window.__init__(self, title="Central Control")
#         self.set_default_size(400, 400)
#         self.set_default_geometry
#         self.set_border_width(10)
#         listbox = Gtk.ListBox()
#         listbox.set_selection_mode(Gtk.SelectionMode.NONE)
#         self.add(listbox)
#
#         #Generates the reset label and button
#         reset_row = Gtk.ListBoxRow()
#         reset_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=100)
#         reset_row.add(reset_box)
#         reset_label = Gtk.Label("Reset the whole system")
#         reset_label.set_markup("<big>Reset the whole system</big>")
#         reset_button = Gtk.Button("Reset")
#         reset_box.pack_start(reset_label, True, True, 0)
#         reset_box.pack_start(reset_button, True, True, 0)
#         listbox.add(reset_row)
#
#         #LED 1 label and the switch
#         led_row1 = Gtk.ListBoxRow()
#         led_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=100)
#         led_row1.add(led_box)
#         led1_label = Gtk.Label("Room 1 LED Status")
#         led_button_room_1 = Gtk.Switch()
#         led_box.pack_start(led1_label, True, True, 0)
#         led_box.pack_start(led_button_room_1, True, True, 0)
#         listbox.add(led_row1)
#
#         #LED 2 label and the switch
#         led_row2 = Gtk.ListBoxRow()
#         led_box2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=100)
#         led_row2.add(led_box2)
#         led1_label2 = Gtk.Label("Room 2 LED Status")
#         led_button_room_2 = Gtk.Switch()
#         led_box2.pack_start(led1_label2, True, True, 0)
#         led_box2.pack_start(led_button_room_2, True, True, 0)
#         listbox.add(led_row2)
#
#         #Song indicator bar
#         song_row = Gtk.ListBoxRow()
#         song_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=100)
#         song_row.add(song_box)
#         song_label = Gtk.Label("Song status:")
#         song_box.pack_start(song_label, True, True, 0)
#         #song_box.pack_start(led_button_room_2, True, True, 0)
#         listbox.add(song_row)

#--------------------------------------------------------------------------------
#change HOST_IP to current device IP
HOST_IP = '10.0.1.18'

class ControllerCommunication(object):
    def __init__(self):
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
        return "got message form Room"
        print "emit a signal to GUI"


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
    channel1.start_consuming()
    # Gtk.main()
except SystemExit:
    #Unregiste service form local network when system Exit.
    print "Unregistering..."
    zeroconf.unregister_service(info)
    zeroconf.close()

