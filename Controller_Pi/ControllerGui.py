#This is a controller GUI Program
import socket, pika
#Uncomment the next line to enable GUI import
from gi.repository import Gtk
from zeroconf import *


class MainWindow(Gtk.Window):

    def __init__(self):
        """
        constructor, generates the base layout of the central control unit
        :return:
        """
        #Set the window size and border and list box layout
        Gtk.Window.__init__(self, title="Central Control")
        self.set_default_size(400, 400)
        self.set_default_geometry
        self.set_border_width(10)
        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.add(listbox)

        #Generates the reset label and button
        reset_row = Gtk.ListBoxRow()
        reset_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=100)
        reset_row.add(reset_box)
        reset_label = Gtk.Label("Reset the whole system")
        reset_label.set_markup("<big>Reset the whole system</big>")
        reset_button = Gtk.Button("Reset")
        reset_box.pack_start(reset_label, True, True, 0)
        reset_box.pack_start(reset_button, True, True, 0)
        listbox.add(reset_row)

        #LED 1 label and the switch
        led_row1 = Gtk.ListBoxRow()
        led_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=100)
        led_row1.add(led_box)
        led1_label = Gtk.Label("Room 1 LED Status")
        led_button_room_1 = Gtk.Switch()
        led_box.pack_start(led1_label, True, True, 0)
        led_box.pack_start(led_button_room_1, True, True, 0)
        listbox.add(led_row1)

        #LED 2 label and the switch
        led_row2 = Gtk.ListBoxRow()
        led_box2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=100)
        led_row2.add(led_box2)
        led1_label2 = Gtk.Label("Room 2 LED Status")
        led_button_room_2 = Gtk.Switch()
        led_box2.pack_start(led1_label2, True, True, 0)
        led_box2.pack_start(led_button_room_2, True, True, 0)
        listbox.add(led_row2)

        #Song indicator bar
        song_row = Gtk.ListBoxRow()
        song_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=100)
        song_row.add(song_box)
        song_label = Gtk.Label("Song status:")
        song_box.pack_start(song_label, True, True, 0)
        #song_box.pack_start(led_button_room_2, True, True, 0)
        listbox.add(song_row)

#--------------------------------------------------------------------------------

#connect Controller GUI to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='control_queue')#declare queue name as control_queue

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

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='control_queue')
#--------------------------------------------------------------------------------

# Make a instence of the mainwindow class
win = MainWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()

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
    start consuming message from control_queue
    channel.start_consuming()
    Gtk.main()
except SystemExit:
    #Unregiste service form local network when system Exit.
    print "Unregistering..."
    zeroconf.unregister_service(info)
    zeroconf.close()
    socket.gethostbyname()

