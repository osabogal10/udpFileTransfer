import socket, threading, os, hashlib,sys
from time import sleep


SIZE=60000
hasher = hashlib.md5()
# Create a UDP socket

class udp_transfer:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to the port
    def __init__(self):
        server_address = ('157.253.205.7', 10000)
        num_clients = int(sys.argv[1])
        file_name = sys.argv[2]

        print('starting up on {} port {}'.format(*server_address))

        print('Argument List:', str(sys.argv))
        self.sock.bind(server_address)
        self.sock.setblocking(True)
        print('\nwaiting to receive message')
        threads = []
        id_cliente =1
        while num_clients > 0:
            data, address =self. sock.recvfrom(SIZE)
            if data == b'Listo':
                size = os.path.getsize(file_name)
                print(' file size : {}'.format(str(size)))

                send_thread = threading.Thread(target=self.send_file, args=( address, file_name, id_cliente))
                threads.append(send_thread)
                num_clients = num_clients-1
                id_cliente =id_cliente+1
                print(num_clients)
        for thread in threads:
            thread.start()

    def send_file(self, address, file_name, id_cliente):
        i = 0
        size = os.path.getsize(file_name)
        bytesSent = 0
        print(' file size : {}'.format(str(size)))
        with open(file_name, 'rb') as file:
            data = file.read(SIZE)
            while data != bytes(''.encode()):
                sent = self.sock.sendto(data, address)
                data = file.read(SIZE)
                #print('data',data)
                #print('{}. sent {} bytes back to {}'.format(i,sent, address))
                i = i +1
                bytesSent = bytesSent+sent
                if sent != SIZE:
                    sent = self.sock.sendto(b'Fin', address)
                    print('Fin')
                    #print('sent {} bytes back to {}'.format(sent, address))
                    break
            buf = file.read()
            hasher.update(buf)
            hash_servidor = hasher.hexdigest()

            self.sock.sendto(file_name.encode('utf-8'), address)
            self.sock.sendto(str(os.path.getsize(file_name)).encode('utf-8'), address)
            self.sock.sendto(str(id_cliente).encode('utf-8'), address)
            self.sock.sendto(str(hash_servidor).encode('utf-8'), address)
            self.sock.sendto(str(bytesSent).encode('utf-8'), address)
            self.sock.sendto(str(i).encode('utf-8'), address)








udp = udp_transfer()

