from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM

from bridgecastlib.receiver import BaseReceiver

class VNCReceiverServer(Thread):
    def __init__(self, bridge, port):
        Thread.__init__(self, name="VNCReceiverServerThread")
        self._bridge = bridge
        self._port = port
    
    def run(self):
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._socket.bind(("0.0.0.0", self._port))
        self._socket.listen()
        
        while True:
            (clientsocket, address) = self._socket.accept()

            re = VNCReceiver(self._bridge, clientsocket)
            self._bridge.addReceiver(re)
            re.start()

class VNCReceiver(BaseReceiver):
    def run(self):
        while True:
            data = self._socket.recv(4096);
            print(data)
            if data == b"":
                self._socket.close()
                return