from threading import Thread
from time import sleep

from bridgecastlib.receiver.VNCReceiver import VNCReceiverServer
from bridgecastlib.sender.ReverseVNCSender import ReverseVNCSenderServer
from bridgecastlib.Command import CommandServer

class Bridge(Thread):
    def __init__(self):
        Thread.__init__(self, name="Bridge")
        self._senders = []
        self._receivers = []
        self._servers = []

    def addSender(self, sender):
        if not sender in self._senders:
            self._senders.append(sender)

    def addReceiver(self, receiver):
        if not receiver in self._receivers:
            self._receivers.append(receiver)

    def run(self):
        print("Setting up BridgeCast...")
        self._servers.append(VNCReceiverServer(self, 5900))
        #self._servers.append(ReverseVNCSenderServer(self, 5901))

        print("Starting Servers...")
        for s in self._servers:
            s.start()

        print("Start Command Server...")
        cServer = CommandServer("", 80, self)
        cServer.start()

        while True:
            rr = 0
            for r in self._receivers:
                if not r.isAlive():
                    self._receivers.remove(r)
                    rr += 1

            rs = 0
            for s in self._senders:
                if not s.isAlive():
                    self._senders.remove(s)
                    rs += 1

            print("Bridge Cleanup removed %d Receivers and %d Senders" % (rr, rs))
            print("Bridge Tick (Receivers: %d; Senders: %d)" % (len(self._receivers), len(self._senders)))
            sleep(5)