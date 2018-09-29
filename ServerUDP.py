import socket
import sys
import time
import hashlib

def read_in_chunks(file_object, chunk_size=1024):
    while True:
        chunk_data = file_object.read(chunk_size)
        if not chunk_data:
            break
        yield chunk_data

def getSize(file_object):
    file_object.seek(0,2)
    size = file_object.tell()
    file_object.seek(0)
    return size

def md5Sum(filename, blocksize=1024):
    hash = hashlib.md5()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(blocksize), b''):
            hash.update(block)
    return hash.hexdigest()

Multicast_group = ('224.0.0.1',9001)
Server_IP = (input('IP del servidor:'),9000)
Clients = 0
Clients_to_join = int(input('Numero de clientes:'))
buffer_size = 1024
file_path = './dataServer/homero.jpg'
addr = []

try:
    unicast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('')
    print('Socket unicast creado')
except socket.error:
    print('Fallo al crear socket unicast')
    sys.exit()

try:
    unicast.bind(Server_IP)
    print('Bind de unicast completo')
except socket.error:
    print('Fallo bind de unicast')
    sys.exit()

try:
    multicast = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    print('Socket Multicast creado')
except socket.error:
    print('Error al crear socket multicast')
    sys.exit()

print('Esperando resuesta del cliente')

while Clients < Clients_to_join:
    d = unicast.recvfrom(buffer_size)
    data = d[0]
    addr = d[1]

    reply = 'Espere la transferencia (?'

    unicast.sendto(reply.encode('utf-8'), addr)

    print('')
    print('Respuesta del cliente desde: [', addr[0],': ',str(addr[1]),'] = ',data.strip())

    Clients = Clients + 1

if Clients == Clients_to_join:
    print('')
    print('- Enviando datos al siguiente grupo: ', str(Multicast_group))
    print('- Enviando el siguiente archivo: ', str(file_path))

    bytes = open(file_path)
    size = getSize(bytes)

    multicast.sendto(str(size), Multicast_group)

    for pieza in read_in_chunks(bytes, 1024):
        multicast.sendto(pieza, Multicast_group)
        time.sleep(0.02)

    hashsum = md5Sum(file_path)

    print('')
    print('Hash : ', hashsum)

    print('')
    print('Enviando datos ... ESPERE! ')

try:
    unicast.close()
    print('')
    print('Socket unicast cerrado OK')
except socket.error:
    print('Fallo al cerrar el socket')
    sys.exit()

print('THE END :v')