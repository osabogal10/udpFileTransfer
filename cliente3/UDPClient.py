import socket, os, sys, threading, hashlib

from time import sleep

SIZE=2048
hasher = hashlib.md5()
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10000)
message = b'Listo'

try:
    # Send data
    print('sending {!r}'.format(message))
    sent = sock.sendto(message, server_address)

    #data = sock.recv(1024)
    filename = './recibido/newfile1.jpg'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    i = 0
    with open(filename, 'wb+') as f:
        data, address = sock.recvfrom(SIZE)
        while data != bytes(''.encode()):
            # print(data)
            f.write(data)
            data, address = sock.recvfrom(SIZE)
            # Send data
            print(i,data)
            i = i+1
            print('received {} bytes from {}'.format(len(data), address))

            if data == b'Fin' :
                print('Fin de la wea')
                break
            print('estoy en loop')
            #print(data)
        print('sali de loop')
        buf = f.read()
        hasher.update(buf)
        print('hash: ', hasher.hexdigest())
    print('sali de open (?')
        #sent = sock.sendto(message, server_address)
        # Receive response
        #print('waiting to receive')
        #data, server = sock.recvfrom(4096)
        #print('received {!r}'.format(data))

finally:
    print('closing socket')
    sock.close()
