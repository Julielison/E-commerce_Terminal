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

    
    def adicionarCategoriaEstoque(self) -> dict: #Adiciona uma categoria ao estoque
        categoria = input("Digite a categoria que deseja adicionar ao estoque: ")
        self.__adicionarCategoriaEstoque(categoria)
        return self.estoque
    

    def adicionarProdutoEstoque(self) -> dict: #Adiciona um produto a uma categoria do estoque
        categoria = input("Digite a categoria do produto: ")
        produto = input("Digite o nome do produto: ")
        preco = float(input("Digite o preco do produto: "))
        quantidade = int(input("Digite a quantidade do produto: "))
        self.__adicionarProdutoEstoque(categoria, produto, preco, quantidade)
        return self.estoque
    
    def removerProdutoEstoque(self) -> dict: #Remove um produto de uma categoria do estoque
        categoria = input("Digite a categoria do produto que deseja remover: ")
        produto = input("Digite o nome do produto que deseja remover: ")
        self.removerProdutoEstoque(categoria, produto)
        return self.estoque
    
    
    def __createList(self, categoria:str) -> list: #Cria uma lista vazia para uma categoria do estoque
        self.estoque[categoria] = list()
        return self.estoque[categoria]
    
    def __adicionarCategoriaEstoque(self, categoria:list ) -> list :  #Adiciona uma categoria ao estoque 
        listCategoria = self.__createList(categoria)
        self.estoque[categoria] = listCategoria
        return self.estoque
    
    def __adicionarProdutoEstoque(self, categoria:str, produto:str, preco:float, quantidade:int) -> dict: #Adiciona um produto a uma categoria do estoque(Corrigir)        
        self.estoque[categoria] = {"produto":produto, "preco":preco, "quantidade":quantidade} # Consertar essa linha (não está adicionando o produto mais de um produto)
  
        return self.estoque
    
    def removerProdutoEstoque(self, categoria:str, produto:str) -> dict: #Remove um produto de uma categoria do estoque
        categoria = input("Digite a categoria do produto que deseja remover: ")
        produto = input("Digite o nome do produto que deseja remover: ")
        del self.estoque[categoria][produto]
        return self.estoque
    
    def listarEstoque(self) -> dict: #Lista o estoque
        print(self.estoque)
        return self.estoque
    

    def interface(self) -> None:
        threading.Thread(target=self.__interfaceEstoque).start()
        return None

    
    def __interfaceEstoque(self) -> None:
        print(f"Bem vindo ao sistema de estoque ")
        print(f" Selecione a opção desejada")
        print("1 - Adicionar categoria ao estoque")
        print("2 - Adicionar produto ao estoque")
        print("3 - Remover produto do estoque")
        print("4 - Listar estoque")
        print("5 - Sair")

        options = {'1':self.adicionarCategoriaEstoque, '2':self.adicionarProdutoEstoque, '3':self.removerProdutoEstoque, '4':self.listarEstoque, '5':sys.exit}
        
        while True:
            option = input("Digite a opcao desejada: ")
            if option in options:
                options[option]()
            else:
                print("Opção inválida. Tente novamente.")
            
            if option == '5':
                break
        return None


if __name__ == '__main__':
    servidor = Servidor()
    servidor.start()
    servidor.interface()


