import pika, socket, uuid, json
from zeroconf import *

#!/usr/bin/env python
__author__ = 'jason'


#This class will handle all the communication within the room pi.
#It also need to handle the communication between controller pi and client pi
class Communicator(object):
    def __init__(self):
        self.Client_Connected = False
        self.Controller_Connected = False
        self.Client_Command = ''
        self.Controller_Address = ''
        #setup RabbitMQ Config
        # self.connection = pika.BlockingConnection(pika.ConnectionParameters(
        #         host='localhost'))
        #
        # self.channel = self.connection.channel()
        #
        # result = self.channel.queue_declare(exclusive=True)
        # self.callback_queue = result.method.queue
        #
        # self.channel.basic_consume(self.on_response, no_ack=True,
        #                            queue=self.callback_queue)
        #when communicator initialed, it will try to connect controller pi
        self._ControllerConnect_()


    #This function will try to connect Controller pi
    def _ControllerConnect_(self):
        print "test controller zeroconfig"
        zeroconf = Zeroconf()
        listener = MyListener_Controller()
        binfo = listener.add_service(zeroconf,"_http._tcp.local.","Controller_http._tcp.local.")
        #will use a thread to handle connection between room pi and controler pi
        if binfo is not None:
            print "Controller host is ", binfo.bhost
            print "Controller proper is ", binfo.bproper
            self.Controller = ControllerMQ()
            self.Controller_Connected = True
        else:
            print 'Did not found Controller pi!'

    #This function will try to connect Client pi
    def _ClientConnect_(self):
        print "test client zeroconfig"
        zeroconf = Zeroconf()
        listener = MyListener_Client()
        binfo = listener.add_service(zeroconf,"_http._tcp.local.","Controller_http._tcp.local.")
        #will use a thread to handle connection between room pi and controler pi
        if binfo is not None:
            print "Clinet host is ", binfo.bhost
            print "Client proper is ", binfo.bproper
            self.Client = ClientMQ(binfo.bhost)
            self.Client_Connected = True
        else:
            print 'Did not found Client pi!'

    def _MusicPlayerInfo_(self, cSong, cIns):
        self.MusicInfo = {"Track": cSong, "TrackStatus": cIns}
        self.Controller.call(json.dumps(self.MusicInfo))

    def _LEDInfo_(self, led):
        self.LED_Status = {"LEDStatus": led}
        self.Controller.call(json.dumps(self.LED_Status))

    def DisconnectClient(self):
        self.Client.disconnect()







#zero config for controller pi, this listener is a filter that only return Controller's service information
class MyListener_Controller(object):

    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        print info
        if info is not None:
            #print info.get_Server()
            if info.get_Server() == "Controller.":
                bottleinfo = setinfo(str(socket.inet_ntoa(info.get_Address())),info.get_Properties())
                return bottleinfo

#zero config for Clinet pi, this listener is a filter that only return Client's service information
class MyListener_Client(object):

    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        print info
        if info is not None:
            #print info.get_Server()
            if info.get_Server() == "Client.":
                bottleinfo = setinfo(str(socket.inet_ntoa(info.get_Address())),info.get_Properties())
                return bottleinfo

#Zero config helper function, will store host address and properties
class setinfo(object):
    def __init__(self,bhost,bproper):
        self.bhost = bhost
        self.bproper = bproper

#Controller pi RabbitMQ sender
class ControllerMQ(object):
    def __init__(self,chost):
        self.Controll_host = chost
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=self.Controll_host))

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
                                   routing_key='control_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=n)
        while self.response is None:
            self.connection.process_data_events()
        return self.response

#Client rabbitMQ sender, will receive service information from zero config
class ClientMQ(object):
    def __init__(self,chost):
        self.Client_host = chost
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=self.Client_host))

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
                                   routing_key='client_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=n)
        while self.response is None:
            self.connection.process_data_events()
        return self.response

    def disconnect(self):
        self.connection.close()

communicate = Communicator()