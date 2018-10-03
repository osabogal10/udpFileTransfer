import socket, threading, os, hashlib
from time import sleep

SIZE=2048
hasher = hashlib.md5()
# Create a UDP socket

class udp_transfer:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the port
    def __init__(self):
        server_address = ('localhost', 10000)
        print('starting up on {} port {}'.format(*server_address))
        self.sock.bind(server_address)
        print('\nwaiting to receive message')
        threads = []
        while True:
            data, address =self. sock.recvfrom(SIZE)
            if data == b'Listo':
                file_name = 'imac.jpg'
                size = os.path.getsize(file_name)
                print(' file size : {}'.format(str(size)))

                send_thread = threading.Thread(target=self.send_file, args=( address,))
                send_thread.start()

    def send_file(self, address):
        file_name = 'imac.jpg'
        i = 0
        size = os.path.getsize(file_name)
        print(' file size : {}'.format(str(size)))
        with open(file_name, 'rb') as file:
            data = file.read(SIZE)
            while data != bytes(''.encode()):
                sent = self.sock.sendto(data, address)
                data = file.read(SIZE)
                print('data',data)
                print('{}. sent {} bytes back to {}'.format(i,sent, address))
                i = i +1
                if sent != SIZE:
                    sent = self.sock.sendto(b'Fin', address)
                    print('Fin')
                    print('sent {} bytes back to {}'.format(sent, address))
                    break
            buf = file.read()
            hasher.update(buf)
            print(hasher.hexdigest())

udp = udp_transfer()

