import socket
import sys
import os
import time
import threading

class Cliente:
    def __init__(self):
        self.host = 'localhost'
        self.port = 55550
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self): # Inicia o cliente e conecta ao servidor realiza a troca de mensagens de forma assíncrona (Cria uma thread para enviar mensagens e outra para receber mensagens)
        self.socket.connect((self.host, self.port))
        print('Conectado ao servidor')
        threading.Thread(target=self.send_message).start()
        threading.Thread(target=self.receive_message).start()
 
    def send_message(self): # Envia mensagens para o servidor
        while True:
            message = input()
            self.socket.sendall(message.encode())
            if message == 'exit':
                self.socket.close()
                break

    def receive_message(self): # Recebe mensagens do servidor
        while True:
            data = self.socket.recv(1024)
            print('Recebido:', data.decode().split('@#'))
            if data.decode() == 'exit':
                self.socket.close()
                break

if __name__ == '__main__':
    cliente = Cliente()
    cliente.start()