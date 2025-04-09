# network.py
import socket
import threading

class UDPNetwork:
    def __init__(self, is_server=False, ip='127.0.0.1', port=12000):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(False)
        self.addr = (ip, port)
        self.is_server = is_server
        self.remote_addr = None
        self.messages = []

        if is_server:
            self.sock.bind(self.addr)

        self.running = True
        self.thread = threading.Thread(target=self.listen)
        self.thread.start()

    def listen(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(4096)
                message = data.decode()
                self.messages.append((addr, message))
                if self.is_server and not self.remote_addr:
                    self.remote_addr = addr
            except:
                pass

    def send(self, message):
        if self.is_server:
            if self.remote_addr:
                self.sock.sendto(message.encode(), self.remote_addr)
        else:
            self.sock.sendto(message.encode(), self.addr)

    def get_messages(self):
        msgs = self.messages[:]
        self.messages.clear()
        return msgs

    def stop(self):
        self.running = False
        self.thread.join()
        self.sock.close()
