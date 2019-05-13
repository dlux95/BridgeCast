from threading import Thread

class BaseReceiverServer(Thread):
    pass

class BaseReceiver(Thread):
    def __init__(self, bridge, socket):
        Thread.__init__(self, name="%s:%s" % (str(self.__class__.__name__), socket.getpeername()))
        self._bridge = bridge
        self._socket = socket

    def attachFB(self, fb):
        self._fb = fb

    def detachFB(self):
        self._fb = None