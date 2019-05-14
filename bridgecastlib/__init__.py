
class SocketHelper(object):
    def receive_bytes(self, i):
        b = self._socket.recv(i)
        if not b:
            raise Exception("Socket closed")
        return b


    def receive_uint8(self):
        return int.from_bytes(self.receive_bytes(1), byteorder="big", signed=False)
    def receive_int8(self):
        return int.from_bytes(self.receive_bytes(1), byteorder="big", signed=True)

    def receive_uint16(self):
        return int.from_bytes(self.receive_bytes(2), byteorder="big", signed=False)
    def receive_int16(self):
        return int.from_bytes(self.receive_bytes(2), byteorder="big", signed=True)

    def receive_uint32(self):
        return int.from_bytes(self.receive_bytes(4), byteorder="big", signed=False)
    def receive_int32(self):
        return int.from_bytes(self.receive_bytes(4), byteorder="big", signed=True)

    def receive_uint64(self):
        return int.from_bytes(self.receive_bytes(8), byteorder="big", signed=False)
    def receive_int64(self):
        return int.from_bytes(self.receive_bytes(8), byteorder="big", signed=True)

    def send_uint8(self, i):
        self._socket.send(int.to_bytes(i, 1, byteorder="big", signed=False))
    def send_int8(self, i):
        self._socket.send(int.to_bytes(i, 1, byteorder="big", signed=True))

    def send_uint16(self, i):
        self._socket.send(int.to_bytes(i, 2, byteorder="big", signed=False))
    def send_int16(self, i):
        self._socket.send(int.to_bytes(i, 2, byteorder="big", signed=True))

    def send_uint32(self, i):
        self._socket.send(int.to_bytes(i, 4, byteorder="big", signed=False))
    def send_int32(self, i):
        self._socket.send(int.to_bytes(i, 4, byteorder="big", signed=True))

    def send_uint64(self, i):
        self._socket.send(int.to_bytes(i, 8, byteorder="big", signed=False))
    def send_int64(self, i):
        self._socket.send(int.to_bytes(i, 8, byteorder="big", signed=True))

    def receive_byte(self):
        return self._socket.recv(1)

    def send_byte(self, b):
        self._socket.send(b)