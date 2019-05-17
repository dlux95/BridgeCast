from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM
import math

from bridgecastlib.VirtualFB import VirtualFB
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
    def __init__(self, bridge, sock):
        BaseReceiver.__init__(self, bridge, sock)
        self._fb = VirtualFB(1280, 720, 32)

    def send_hello(self):
        self.send_byte(b"RFB 003.003\n")

    def send_security(self):
        self.send_uint16(0)
        self.send_uint16(1)

    def send_init(self):
        self.send_uint16(1280) # X
        self.send_uint16(720) # Y
        self.send_uint8(32) # Bits per pixel
        self.send_uint8(32) # depth
        self.send_uint8(1) # big endian
        self.send_uint8(1) # true color
        self.send_uint16(255) # max red
        self.send_uint16(255) # max green
        self.send_uint16(255) # max blue
        self.send_uint8(0) # shift red
        self.send_uint8(0) # shift green
        self.send_uint8(0) # shift blue
        self.send_byte(b"\x00\x00\x00") # padding
        
        name = "BridgeCast VNCReceiver"
        self.send_uint32(len(name))
        self.send_byte(bytes(name, "ascii"))

    def handle_set_pixelformat(self):
        #print("Handle Set Pixelformat")
        self.receive_bytes(19)

    def handle_set_encoding(self):
        #print("Handle Set Encoding")
        self.receive_bytes(1)
        encodingnum = self.receive_uint16()
        for i in range(encodingnum):
            self.receive_int32()

    def handle_framebuffer_update_request(self):
        #print("Handle Framebuffer Update Request")
        self.receive_bytes(9)

    def handle_key_event(self):
        #print("Handle Key Event")
        self.receive_bytes(7)

    def handle_pointer_event(self):
        #print("Handle Pointer Event")
        self.receive_bytes(5)

    def handle_client_cut_text(self):
        #print("Handle Client Cut Text")
        self.receive_bytes(3)
        l = self.receive_uint32()
        text = self.receive_bytes(l)

    def run(self):
        self.send_hello()
        print("Hello: ", self._socket.recv(12))

        self.send_security()
        print("Security: ", self.receive_uint8())
        
        self.send_init()

        x = 0
        y = 0

        test = [255 for i in range(50*50*4)]
        self._fb.fill_rect(100, 100, 50, 50, bytearray(test))

        while True:
            opcode = self.receive_uint8();

            if opcode == 0:
                self.handle_set_pixelformat()
            if opcode == 2:
                self.handle_set_encoding()
            if opcode == 3:
                self.handle_framebuffer_update_request()
            if opcode == 4:
                self.handle_key_event()
            if opcode == 5:
                self.handle_pointer_event()
            if opcode == 6:
                self.handle_client_cut_text()

            if self._fb.dirty:
                print("FrameBuffer is dirty. Sending it")
                self.send_uint8(0)
                self.send_uint8(0)
                self.send_uint16(1)

                self.send_uint16(x)
                self.send_uint16(y)
                self.send_uint16(1280)
                self.send_uint16(720)
                self.send_int32(0)

                self.send_byte(self._fb.get_rect(x, y, 1280, 720))
                self._fb.dirty = False