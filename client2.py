import socket
from _thread import *
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP_address = 'localhost'
Port = 8080
server.connect((IP_address, Port))
changer = True


def cryptographyOfCesar(text, change):
    ascii_values = []
    encrypted_string = ''
    for character in text:
        ascii_values.append(ord(character) + change)

    for character in ascii_values:
        encrypted_string += chr(character)

    return encrypted_string


def receiveMessage():
    while True:
        message = server.recv(2048)
        decrypted_msg = cryptographyOfCesar(message.decode(), -3)
        print(decrypted_msg + "\n")


def sendMessage():
    while True:
        message = input("")
        encrypted_msg = cryptographyOfCesar(message, 3)
        server.send(encrypted_msg.encode("utf-8"))


start_new_thread(receiveMessage, ())

start_new_thread(sendMessage, ())

while True:
    time.sleep(5)