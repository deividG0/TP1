import socket
from _thread import *
import time
import sys

print(sys.argv)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# IP_address = sys.argv[1]
# Port = int(sys.argv[2])
# fileName = sys.argv[3]
IP_address = 'localhost'
Port = 8080
file_name = 'file6.txt'
server.connect((IP_address, Port))


def receiveMessage():
    data = server.recv(2048).decode("utf-8")
    print(data)
    if len(data) <= 0: # Deve ter uma melhor forma de verificar se o arquivo nao existe
        print(f"File {file_name} does not exist in the server")
    else:
        file = open(file_name, "w")
        file.write(data)
        print(f"File {file_name} saved")
        file.close()


def sendMessage():
    # message = input("")
    try:
        server.send(file_name.encode("utf-8"))
    except Exception as e:
        print(e)


start_new_thread(receiveMessage, ())

start_new_thread(sendMessage, ())

while True:
    time.sleep(5)