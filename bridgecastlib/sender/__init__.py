from threading import Thread

class BaseSenderServer(Thread):
    pass

class BaseSender(object):
    def attachFB(self, fb):
        self._fb = fb

    def detachFB(self):
        self._fb = None
    