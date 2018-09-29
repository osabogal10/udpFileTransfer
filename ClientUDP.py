import socket
import sys
import hashlib

def md5Sum(filename, blocksize=1024):
    hash = hashlib.md5()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(blocksize), b''):
            hash.update(block)
    return hash.hexdigest()

Multicast_group = ('224.0.0.1',9001)
Server_IP = (input('IP del servidor:'),9000)
buffer_size = 1024


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



try:
    unicast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('')
    print('Socket unicast creado')
except socket.error:
    print('Fallo al crear socket unicast')
    sys.exit()

try:
    multicast = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    print('Socket Multicast creado')
except socket.error:
    print('Error al crear socket multicast')
    sys.exit()

try:
    multicast.bind(Multicast_group)
    print('Bind de Multicast completo')
except socket.error:
    print('Fallo bind de Multicast')
    sys.exit()

print('Esperando resuesta del servidor')

Message = 'Esperando para recibir datos...'

try:
    unicast.sendto(Message.encode('utf-8'), Server_IP)
    d = unicast.recvfrom(buffer_size)
    reply = d[0]
    addr = d[1]

    print('')
    print('Respuesta del servidor: ',reply)
except socket.error:
    print('El servidor no responde')
    sys.exit()

size, Multicast_group = multicast.recvfrom(buffer_size)
size = int(size)

print('')
print('Tamaño del archivo: ', str(size))
print('')

file = open('./dataClient/homeroRecibido.jpg', 'w')
file_path = './dataClient/homeroRecibido.jpg'

total = 0
while True:
    pieza, Multicast_group_loop = multicast.recvfrom(buffer_size)
    file.write(pieza)

    total += len(pieza)
    print('Tamaño actual recibido: ',str(total))
    if total == size:
        break

file.close()
hashsum = md5Sum(file_path)

print('')
print('Hash : ', hashsum)

print('')
print('Transferencia terminada.')


try:
    unicast.close()
    print('')
    print('Socket unicast cerrado OK')
except socket.error:
    print('Fallo al cerrar el socket')
    sys.exit()

try:
    multicast.close()
    print('')
    print('Socket multicast cerrado OK')
except socket.error:
    print('Fallo al cerrar el socket')
    sys.exit()

print('THE END Cliente :v')