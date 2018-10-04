import socket, os, sys, threading, hashlib, time, logging
from time import gmtime, strftime

from sys     import stderr
import logging
from logging import getLogger, StreamHandler, Formatter, DEBUG

l  = getLogger()
os.makedirs(os.path.dirname('./logs/UDP.log'), exist_ok=True)
logging.basicConfig(format='%(message)s', filename='./logs/UDP.log',  level=logging.DEBUG)
sh = StreamHandler(stderr)
sh.setLevel(DEBUG)
f  = Formatter(' %(message)s')
sh.setFormatter(f)
l.addHandler(sh)
l.setLevel(DEBUG)



SIZE=60000
hasher = hashlib.md5()
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10000)
message = b'Listo'
showtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
l.info('%s;%s','DATE',showtime)


try:
    # Send data
    print('Connected successfully')
    print('sending {!r}'.format(message))
    sent = sock.sendto(message, server_address)
    start_time = time.time()
    #data = sock.recv(1024)
    filename = './recibido/newfile1.mp3'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    i = 0
    bytesReceived = 0
    with open(filename, 'wb+') as f:
        data, address = sock.recvfrom(SIZE)
        while data != bytes(''.encode()):
            # print(data)
            f.write(data)
            data, address = sock.recvfrom(SIZE)
            # Send data
            #print(i,data)
            i = i+1
            #print('received {} bytes from {}'.format(len(data), address))
            bytesReceived = bytesReceived + len(data)

            if data == b'Fin':
                bytesReceived = bytesReceived + len(data)
                print('Over')
                break


        buf = f.read()
        hasher.update(buf)
        hash_cliente = hasher.hexdigest()
        print('hash_ cliente: ', hasher.hexdigest())
        rcv_file_name, address = sock.recvfrom(SIZE)

        l.info('%s;%s', 'FILE_NAME', rcv_file_name.decode('utf-8'))

        rcv_file_size, address = sock.recvfrom(SIZE)
        l.info('%s;%s', 'FILE_SIZE',rcv_file_size.decode('utf-8'))

        miIdCliente, address = sock.recvfrom(SIZE)
        l.info('%s;%s', 'CLIENT', miIdCliente.decode('utf-8'))

        hash_servidor, address = sock.recvfrom(SIZE)
        hash_servidor = hash_servidor.decode('utf-8')

        print(hash_servidor)

        if hash_servidor == hash_cliente:
            l.info('FILE_DELIVERY;SUCCESS')
        else:
            l.info('FILE_DELIVERY;FAILURE')

        bytesSent, address = sock.recvfrom(SIZE)
        bytesSent = bytesSent.decode('utf-8')
        l.info('%s;%s', 'BYTES_SENT',bytesSent)

        l.info('%s;%s', 'BYTES_RECEIVED', bytesReceived)

        numPaquetesServ, address = sock.recvfrom(SIZE)
        numPaquetesServ = numPaquetesServ.decode('utf-8')
        numPaquetesCli = i

        l.info('%s;%s', 'PACKETS SENT', numPaquetesServ)
        l.info('%s;%s', 'PACKETS RECEIVED', i)


finally:
    print('closing socket')
    elapsed_time = time.time() - start_time
    l.info('%s;%s','ELAPSED_TIME', elapsed_time)
    l.info('------------------------------')

    sock.close()