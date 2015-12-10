from zeroconf import *
import socket, pika, uuid, json

#json format LED example {'sender': 'Client',
#                         'userID': 'jason',
#                         'device': 'LED',
#                         'action': 'OFF',
#                         'target': 'Room1'}

#json format MusicPlayer example {'sender': 'Client',
#                                 'userID': 'icer',
#                                 'device': 'MusicPlayer',
#                                 'action': 'NEXT',
#                                 'target': 'Room1'}

#Client_Communication class will handle the connection between Controller_pi and Client_pi
class Client_Communication(object):
    def __init__(self):
        self.Controller_Connected = False
        self._ControllerConnect_()

    #This function will try to connect Controller pi
    def _ControllerConnect_(self):
        # print "test controller zeroconfig"
        # zeroconf = Zeroconf()
        # listener = MyListener_Controller()
        # binfo = listener.add_service(zeroconf,"_http._tcp.local.","Controller_http._tcp.local.")
        # #will use a thread to handle connection between room pi and controler pi
        # if binfo is not None:
        #     print "Controller host is ", binfo.bhost
        #     print "Controller proper is ", binfo.bproper
            self.Controller = ControllerMQ('172.31.174.131')#binfo.bhost)
            self.Controller_Connected = True
        # else:
        #     print 'Did not found Controller pi!'

    #call this function to send json formatted voice command to Controller
    def _SendVoiceCommand_(self, voicecommand):
        self.Controller.call(voicecommand)



#Controller pi RabbitMQ sender
class ControllerMQ(object):
    def __init__(self,chost):
        self.Controller_host = chost
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=self.Controller_host))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    #send Json information as param@ n
    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='Control_Client_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=n)
        while self.response is None:
            self.connection.process_data_events()
        return self.response



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
                bottleinfo = Setinfo(str(socket.inet_ntoa(info.get_Address())),info.get_Properties())
                return bottleinfo

#Zero config helper function, will store host address and properties
class Setinfo(object):
    def __init__(self,bhost,bproper):
        self.bhost = bhost
        self.bproper = bproper


test = Client_Communication()
print test.Controller.call(json.dumps({'sender': 'Client',
                                       'userID': 'icer',
                                       'device': 'MusicPlayer',
                                       'action': 'PLAY',
                                       'target': ''}))