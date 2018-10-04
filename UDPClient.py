import socket, os, sys, threading, hashlib, time
from time import gmtime, strftime

SIZE=60000
hasher = hashlib.md5()
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10000)
message = b'Listo'

try:
    # Send data
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
            print(i,data)
            i = i+1
            print('received {} bytes from {}'.format(len(data), address))
            bytesReceived = bytesReceived + len(data)
            if data == b'Fin' :
                print('Fin de la wea')
                break
            print('estoy en loop')
            #print(data)
        print('sali de loop')
        buf = f.read()
        hasher.update(buf)
        hash_cliente = hasher.hexdigest()
        print('hash: ', hasher.hexdigest())
        rcv_file_name, address = sock.recvfrom(SIZE)
        print(rcv_file_name.decode('utf-8'))
        miIdCliente, address = sock.recvfrom(SIZE)
        print('CLIENTE: ',miIdCliente.decode('utf-8'))
        hash_servidor, address = sock.recvfrom(SIZE)
        hash_servidor = hash_servidor.decode('utf-8')
        if hash_servidor == hash_cliente:
            print('FILE DELIVERY: SUCCESS')
        else:
            print('FILE DELIVER: FAILURE')
        bytesSent, address = sock.recvfrom(SIZE)
        bytesSent = bytesSent.decode('utf-8')
        print('SENT BYTES: ',bytesSent)
        print('RECEIVED BYTES: ', bytesReceived)
        numPaquetesServ, address = sock.recvfrom(SIZE)
        numPaquetesServ = numPaquetesServ.decode('utf-8')
        numPaquetesCli = i
        print('PACKETS SEND: ', numPaquetesServ)
        print('PACKETS RECEIVED: ', i)


    print('sali de open (?')
    print(os.path.getsize(filename))
        #sent = sock.sendto(message, server_address)
        # Receive response
        #print('waiting to receive')
        #data, server = sock.recvfrom(4096)
        #print('received {!r}'.format(data))

finally:
    print('closing socket')
    elapsed_time = time.time() - start_time
    showtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print(elapsed_time)
    print(showtime)

    sock.close()
