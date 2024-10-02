import socket
import threading
from tabulate import tabulate
import os

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
            data = data.decode()
            if data == 'exit':
                self.socket.close()
                break
            self.opcoes(data)

    def opcoes(self, data: str) -> None:
        codigo, dados = data.split('@#')
        if codigo in ['PROD-220','PRCA-222','PQAS-224']:
            tabela = [['id','nome', 'preco','quantidade']]

            for p in dados.split('##'):
                tabela.append(p.split('#'))
            # Exibindo a tabela formatada
            print(tabulate(tabela, headers="firstrow", tablefmt="grid"))

        elif codigo == 'CATE-221':
            tabela = [['Categorias']]
            for e in dados.split('#'):
                tabela.append([e])

            print(tabulate(tabela, headers="firstrow", tablefmt="grid"))

        elif codigo == 'COMP-223':
            print('Compra finalizada.')


if __name__ == '__main__':
    cliente = Cliente()
    cliente.start()