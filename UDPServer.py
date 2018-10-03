import socket, threading, os
from time import sleep


# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

print('\nwaiting to receive message')
data, address = sock.recvfrom(32768)
if data == b'Listo':
    file_name = 'imac.jpg'
    i = 0
    size = os.path.getsize(file_name)
    print(' file size : {}'.format(str(size)))
    with open(file_name, 'rb') as file:
        data = file.read(32768)
        while data != bytes(''.encode()):
            data = file.read(32768)
            sent = sock.sendto(data, address)
            print(data)
            print('{}. sent {} bytes back to {}'.format(i,sent, address))
            i = i +1
            if sent == 0:
                sent = sock.sendto(b'Fin', address)
                print('sent {} bytes back to {}'.format(sent, address))
                break
