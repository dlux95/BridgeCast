from time import sleep
from bridgecastlib.sender import BaseSender
from bridgecastlib.VirtualFB import VirtualFB

class VirtualDesktopSender(BaseSender):
    def __init__(self, receiver):
        BaseSender.__init__(self)
        self._fb = VirtualFB(1280, 720, 32)

        self._receiver = receiver

        test = [255 for i in range(50*50*4)]
        self._fb.fill_rect(100, 100, 50, 50, bytearray(test))

        self.tx = 0
        self.ty = 0

    def run(self):
        while self._receiver.isAlive():
            test = [255 for i in range(50*50*4)]
            self._fb.fill_rect(self.tx, self.ty, 50, 50, bytearray(test))

            self.tx = self.tx+2
            self.ty = self.ty+1

            self._receiver._fb = self._fb
            self._receiver.dirty = True
            sleep(1/30.0)




    