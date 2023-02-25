import socket
from _thread import *
import os
from cache import *

print(sys.argv)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

IP_address = ''
# Port = int(sys.argv[1])
Port = 8080
# home_folder = sys.argv[2]
home_folder = 'home/dist/homework1/'

server.bind((IP_address, Port))
server.listen(100)

list_of_clients = []
capacity = 64
cache = LRUCache(capacity)


def sendFileFromCache(file_name, connection):
    print(f"Cache hit. File {file_name} sent to the client.")
    connection.send(cache.get(file_name).encode("utf-8"))
    cache.get_cache_order()


def sendFileFromRepo(file_name, connection):
    path = home_folder + file_name
    try:
        file = open(path, 'r')
        content = file.read()
        data_size = os.stat(path).st_size
        if data_size < capacity:
            # Armazenando na cache
            cache.put(key=file_name, content=content, value=data_size)
            cache.get_cache_order()
        else:
            print('Não foi armazenado em cache')

        # Enviando do repositório
        connection.send(content.encode("utf-8"))
        print(f"Cache miss. File {file_name} sent to the client.")
    except:
        print(f"File {file_name} does not exist")
        content = ''
        connection.send(content.encode("utf-8"))


def manageFileRequest(file_name, connection):
    if cache.is_in_cache(file_name):
        sendFileFromCache(file_name, connection)
    else:
        sendFileFromRepo(file_name, connection)


def client_thread(connection, address):
    try:
        file_name = connection.recv(2048).decode()
        if file_name:
            if file_name == 'list':
                connection.send(cache.get_cache_list().encode("utf-8"))
            else:
                print(f"Client {address[0]} is requesting file {file_name}")
                manageFileRequest(file_name, connection)
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