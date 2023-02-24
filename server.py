import socket
from _thread import *
import sys
import os
from cache import *

print(sys.argv)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

IP_address = ''
capacity = 100
# Port = int(sys.argv[1])
Port = 8080
# home_folder = sys.argv[2]
home_folder = 'home/dist/homework1/'

server.bind((IP_address, Port))
server.listen(100)

list_of_clients = []
# cache = dict()
# cache = {'home/dist/homework1/homework1.html': 23}
cache = LRUCache(capacity)

# def getCacheSpaceLeft():
#     size=0
#     for x in cache.values():
#         size+=x
#     return 64-size


def fileInCache(file_name):
    path = home_folder + file_name
    case = False
    print(cache.keys())
    for x in cache.keys():
        if path == x:
            case=True
            break
    return case


def sendFileFromCache(file_name,connection):
    #Aqui a operação está igual a de quando o arquivo não está em cache,
    # mas é aqui que entraria a operação de envio diretamente da cache
    path = home_folder + file_name
    file = open(path, 'r')
    data = file.read()
    dataSize = sys.getsizeof(data)
    print(f'fileSize:{dataSize}')
    print(f'data:{data}')
    print(f'type(data):{type(data)}')
    print(f"Cache hit. File {file_name} sent to the client.")
    connection.send(data.encode("utf-8"))


def sendFileFromRepo(file_name, connection):
    path = home_folder + file_name
    file = open(path, 'r')
    data = file.read()
    data_size = sys.getsizeof(data)

    if data_size < capacity:
        # Armazenando na cache
        cache.put(file_name, data)

    print(f'type(data):{type(data)}')
    print(cache.cache)

    # Enviando do repositório
    connection.send(data.encode("utf-8"))
    print(f"Cache miss. File {file_name} sent to the client.")


def manageFileRequest(file_name, connection):
    path = home_folder+file_name
    if cache.is_in_cache(file_name):
        sendFileFromCache(file_name, connection)
    else:
        sendFileFromRepo(file_name, connection)
    # file_size = float((os.stat(path).st_size / (1024 * 1024)))
    # print(os.stat(path).st_size)
    # print(f'fileSize:{fileSize}mb')
    # print(f'cache:{cache}')
    # if fileInCache(fileName):
    #     sendFileFromCache(fileName,connection)
    # else:
    #     if fileSize<=64 and fileSize<=getCacheSpaceLeft() and getCacheSpaceLeft()>0:
    #         cache[path] = fileSize
    #         sendFileFromRepo(fileName,connection)


def client_thread(connection, address):
    try:
        file_name = connection.recv(2048).decode()
        if file_name:
            print(f"Client {address[0]} is requesting file {file_name}")
            manageFileRequest(file_name,connection)
    except Exception as e:
        print(e)


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)

    print(addr[0] + " connected")

    start_new_thread(client_thread, (conn, addr))