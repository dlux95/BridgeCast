from threading import Thread

from bridgecastlib import SocketHelper

class BaseSenderServer(Thread):
    pass

class BaseSender(Thread, SocketHelper):
    def attachFB(self, fb):
        self._fb = fb

    def detachFB(self):
        self._fb = None
    