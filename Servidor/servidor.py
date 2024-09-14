import threading
import socket
import sys
import os
import time



class Servidor:
    def __init__(self):
        self.host = 'localhost'
        self.port = 55550
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.estoque = dict()	 #Dicionário que armazena o estoque (Implementar um arquivo para armazenar o estoque, para que não seja perdido ao fechar o programa, e carregar o estoque ao abrir o programa novamente) Implementar Estrutura de HASHMAP 
        self.commands = {'1':self.listarEstoque, '5':sys.exit}



    def start (self): # Inicia o servidor
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        print('Servidor executando na porta: ', self.port)
        self.interface()
        while True:
            conn, addr = self.socket.accept()
            print('Conectado a', addr)
            threading.Thread(target=self.handle_client, args=(conn,)).start()
            

    def handle_client(self, conn): # Trata a conexão com o cliente e executa os comandos recebidos do cliente(Cria uma thread para cada cliente)
        interface = 'Bem vindo ao SuperMercadao\n1-Listar Estoque\n'
        conn.sendall(interface.encode())

        while True:
            data = conn.recv(1024)
            if not data:
                break
            print('Recebido:', data.decode())
            if data.decode() in self.commands:
                resultado = self.commands[data.decode()]()
                conn.sendall(str(resultado).encode())
        
            else:
                print('Comando inválido. Tente novamente.')
        
            conn.sendall(data)
        conn.close()


if __name__ == '__main__':
    servidor = Servidor()
    servidor.start()
    servidor.interface()


