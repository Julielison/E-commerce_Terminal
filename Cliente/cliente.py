import socket
import threading
from tabulate import tabulate
import sys
import os

class Cliente:
    def __init__(self):
        self.host = 'localhost'
        self.port = 55550
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.carrinho = []  # Carrinho de compras
        self.produtos = []  # Produtos disponíveis
        self.categorias = []  # Categorias
        self.nome = ""
        self.running = True

    def start(self): 
        try:
            self.socket.connect((self.host, self.port))
            print('Conectado ao servidor')
            threading.Thread(target=self.receive_message).start()  # Inicia thread para receber mensagens
            self.tela_inicial()
        except ConnectionError as e:
            print(f'Erro de conexão: {e}')
            self.socket.close()

    def send_message(self, mensagem):
        self.socket.sendall(mensagem.encode())

    def receive_message(self):
        while self.running:
            try:
                data = self.socket.recv(1024)
                if not data:
                    print("Servidor fechou a conexão.")
                    self.encerrar()
                    break
                mensagem_recebida = data.decode()
                print('Recebido:', mensagem_recebida)
                self.processar_resposta(mensagem_recebida)
            except ConnectionError:
                print('Erro ao receber dados.')
                self.encerrar()

    def processar_resposta(self, mensagem):
        if "PROD-220" in mensagem:
            # Divide a string recebida em partes
            partes = mensagem.split('@#')[1]  # Ignora o código de sucesso
            produtos_raw = partes.split('##')  # Divide cada produto
            self.produtos = []  # Inicializa a lista de produtos

            for produto in produtos_raw:
                # Divide as informações de cada produto
                detalhes = produto.split('#')
                if len(detalhes) == 4:  # Espera 4 elementos: ID, nome, preço, quantidade
                    nome_produto = detalhes[1]
                    preco_produto = float(detalhes[2])
                    quantidade_produto = int(detalhes[3])
                    self.produtos.append([nome_produto, preco_produto, quantidade_produto])
            
            self.exibir_tela_de_compras()
        elif "CATE-221" in mensagem:
            self.categorias = eval(mensagem.split('@#')[1])  # Decodifica as categorias
            self.exibir_categorias()
        elif "SUCESSO-500" in mensagem:
            print("Compra finalizada com sucesso!")
            self.carrinho.clear()
            self.encerrar()
        elif "ERRO-300" in mensagem:
            print("Erro na compra. Estoque insuficiente.")
            # Atualizar o carrinho com base na resposta recebida
        elif "ERRO-303" in mensagem:
            print("Erro na compra: estoque insuficiente para um ou mais itens.")
            # Aqui você pode implementar a lógica para atualizar o carrinho

    def tela_inicial(self):
        self.nome = input("Bem-vindo(a) a loja virtual\nDigite seu nome: ")
        print(f"Olá {self.nome}, digite uma das opções a seguir:")
        self.menu_principal()

    def menu_principal(self):
        while True:
            print("1 - Exibir produtos\n2 - Exibir categorias\nX - Sair da loja")
            opcao = input("Digite a opção: ").strip().lower()

            if opcao == "1":
                self.send_message("PEGAR_PRODUTOS")
            elif opcao == "2":
                self.send_message("PEGAR_CATEGORIAS")
            elif opcao == "x":
                self.send_message("SAIR")
                self.encerrar()
                break
            else:
                print("Opção inválida. Tente novamente.")

    def exibir_tela_de_compras(self):
        while True:
            print("Tela de compras:")
            # Usando tabulate para exibir a tabela de produtos
            table = []
            for i, produto in enumerate(self.produtos, 1):
                nome, preco, quantidade = produto
                table.append([i, nome, preco, quantidade])

            headers = ["Opção", "Produto", "Preço", "Disponíveis"]
            print(tabulate(table, headers, tablefmt="grid"))

            print("M - Mostrar mais produtos\nV - Ver itens do carrinho\nX - Sair da loja")
            
            entrada = input("Digite uma opção e a quantidade separadas por espaço, ex.: 1 2: ").strip().lower()

            if entrada == "m":
                continue
            elif entrada == "v":
                self.ver_carrinho()
            elif entrada == "x":
                self.encerrar()
                break
            else:
                try:
                    opcao, quantidade = entrada.split()
                    opcao = int(opcao)
                    quantidade = int(quantidade)
                    self.adicionar_ao_carrinho(opcao, quantidade)
                except ValueError:
                    print("Entrada inválida, tente novamente.")

    def adicionar_ao_carrinho(self, opcao, quantidade):
        produto_selecionado = self.produtos[opcao - 1]
        nome, preco, disponivel = produto_selecionado
        if quantidade <= disponivel:
            self.carrinho.append([nome, preco, quantidade])
            print(f"{nome} adicionado ao carrinho.")
        else:
            print(f"Quantidade indisponível. Disponível: {disponivel}")

        self.deseja_comprar_mais()

    def deseja_comprar_mais(self):
        escolha = input("Deseja comprar mais? (S/N): ").strip().lower()
        if escolha == "s":
            self.exibir_tela_de_compras()
        elif escolha == "n":
            self.ver_carrinho()
        else:
            print("Opção inválida, retornando para compras.")
            self.exibir_tela_de_compras()

    def ver_carrinho(self):
        print("Seu carrinho de compras:")
        # Usando tabulate para exibir a tabela do carrinho
        table = []
        total = 0
        for item in self.carrinho:
            nome, preco, quantidade = item
            total_item = preco * quantidade
            table.append([nome, preco, quantidade, total_item])
            total += total_item

        headers = ["Produto", "Preço", "Quantidade", "Total"]
        print(tabulate(table, headers, tablefmt="grid"))
        print(f"Total a pagar: R$ {total}")
        self.opcoes_do_carrinho()

    def opcoes_do_carrinho(self):
        print("F - Finalizar compra\nC - Continuar comprando\nX - Sair da loja")
        opcao = input("Digite sua opção: ").strip().lower()
        
        if opcao == "f":
            self.finalizar_compra()  # Chama o método para finalizar a compra
        elif opcao == "c":
            self.exibir_tela_de_compras()  # Retorna para a tela de compras
        elif opcao == "x":
            self.encerrar()  # Encerra o cliente
        else:
            print("Opção inválida.")  # Mensagem para opções não reconhecidas
            self.opcoes_do_carrinho()  # Repetir a solicitação

    def finalizar_compra(self):
        # Formatar a mensagem da compra corretamente
        if not self.carrinho:
            print("Seu carrinho está vazio. Adicione itens antes de finalizar a compra.")
            return

        # Montando a string da compra
        itens_compra = []
        for item in self.carrinho:
            nome, preco, quantidade = item
            itens_compra.append(f"{nome}#{quantidade}")  # Formato: nome#quantidade

        # Enviando a mensagem de compra
        self.send_message(f"COMPRAR {', '.join(itens_compra)}")  # Envia a compra como string

    def exibir_categorias(self):
        print("Categorias disponíveis:")
        # Usando tabulate para exibir a tabela de categorias
        table = []
        for i, categoria in enumerate(self.categorias, 1):
            table.append([i, categoria])

        headers = ["Opção", "Categoria"]
        print(tabulate(table, headers, tablefmt="grid"))

        print("M - Mostrar mais categorias\nV - Ver itens do carrinho\nX - Sair da loja")

        opcao = input("Digite a opção: ").strip().lower()

        if opcao == "v":
            self.ver_carrinho()
        elif opcao == "x":
            self.encerrar()
        else:
            print("Opção inválida.")
            self.exibir_categorias()

    def encerrar(self):
        self.running = False
        print("Volte sempre!")
        self.socket.close()
        exit()

if __name__ == '__main__':
    cliente = Cliente()
    cliente.start()
