import socket
import threading
from tabulate import tabulate

class Cliente:
    def __init__(self):
        self.host = 'localhost'
        self.port = 55550
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nome_cliente = None
        self.carrinho = {}
        self.produtos = {}  # Para armazenar os detalhes dos produtos recebidos
        self.running = True  # Sinalizador para a thread

    def start(self):
        self.socket.connect((self.host, self.port))
        print('Conectado ao servidor')

        # Mensagem de boas-vindas
        self.nome_cliente = input("Bem-vindo ao E-commerce! Por favor, insira seu nome: ")
        print(f"Olá, {self.nome_cliente}! Abaixo estão as opções disponíveis:")

        threading.Thread(target=self.receive_message).start()

        while True:
            self.show_menu()
            opcao = input("\nEscolha uma opção: ")

            if opcao == '5':  # SAIR
                self.running = False  # Define o sinalizador como False
                self.socket.sendall('SAIR'.encode())
                print("Obrigado por usar nosso serviço! Tenha um bom dia!")  # Mensagem de agradecimento
                self.socket.close()
                break
            elif opcao == '1':  # VER PRODUTOS
                self.socket.sendall('PEGAR_PRODUTOS'.encode())
            elif opcao == '2':  # VER CATEGORIAS
                self.socket.sendall('PEGAR_CATEGORIAS'.encode())
            elif opcao == '3':  # ADICIONAR PRODUTO AO CARRINHO
                self.adicionar_ao_carrinho()
            elif opcao == '4':  # FINALIZAR COMPRA
                self.finalizar_compra()
            else:
                print("Opção inválida. Tente novamente.")

    def show_menu(self):
        menu = """
        [1] VER PRODUTOS
        [2] VER CATEGORIAS
        [3] ADICIONAR PRODUTO AO CARRINHO
        [4] FINALIZAR COMPRA
        [5] SAIR
        """
        print(menu)

    def receive_message(self):
        while self.running:  # Continuar enquanto o sinalizador for True
            try:
                data = self.socket.recv(1024)
                if not data:  # Verifica se a conexão foi fechada
                    break
                resposta = data.decode().split('@#')

                # Exibir produtos de forma organizada com Tabulate
                if resposta[0] == 'PROD-220':
                    produtos = [p.split('#') for p in resposta[1:][0].split('##')]
                    headers = ['ID', 'Nome', 'Preço', 'Quantidade']
                    self.produtos = {prod[0]: {'nome': prod[1], 'preco': float(prod[2]), 'estoque': int(prod[3])} for prod in produtos}
                    print(tabulate(produtos, headers, tablefmt="grid"))

                elif resposta[0] == 'CATE-221':  # Ajuste aqui para o novo código
                    categorias = resposta[1].split('#')  # Usar '#' como separador
                    print("\nCategorias disponíveis:")
                    
                    # Cria uma tabela para as categorias
                    categoria_table = [[categoria] for categoria in categorias if categoria.strip()]  # Exclui categorias vazias
                    print(tabulate(categoria_table, headers=['Categorias'], tablefmt="grid"))

                else:
                    print(f"Resposta não reconhecida: {resposta[0]}")
            except Exception as e:
                print("Erro ao receber mensagem do servidor:", str(e))
                break

    def adicionar_ao_carrinho(self):
        try:
            produto_id = input("Insira o ID do produto que deseja adicionar ao carrinho: ")
            quantidade = int(input("Quantidade: "))

            if produto_id not in self.produtos:
                print("ID do produto inválido!")
                return

            if quantidade > self.produtos[produto_id]['estoque']:
                print("Quantidade indisponível em estoque.")
                return

            if produto_id in self.carrinho:
                self.carrinho[produto_id] += quantidade
            else:
                self.carrinho[produto_id] = quantidade

            print(f"Produto {produto_id} adicionado ao carrinho.")
        except Exception as e:
            print("Erro ao adicionar produto ao carrinho:", str(e))

    def finalizar_compra(self):
        if not self.carrinho:
            print("Seu carrinho está vazio!")
            return

        # Exibir os itens do carrinho antes da finalização, incluindo preços
        print("\nSeu carrinho:")
        headers = ['ID do Produto', 'Nome', 'Quantidade', 'Preço Unitário (R$)', 'Subtotal (R$)']
        total = 0
        carrinho_table = []
        for prod_id, qtd in self.carrinho.items():
            nome = self.produtos[prod_id]['nome']
            preco_unitario = self.produtos[prod_id]['preco']
            subtotal = preco_unitario * qtd
            total += subtotal
            carrinho_table.append([prod_id, nome, qtd, f"{preco_unitario:.2f}", f"{subtotal:.2f}"])

        print(tabulate(carrinho_table, headers, tablefmt="grid"))
        print(f"\nTotal da compra: R$ {total:.2f}")

        confirmar = input("\nDeseja finalizar a compra? (s/n): ")
        if confirmar.lower() == 's':
            # Montar a string de compra no formato ID:quantidade;ID:quantidade
            compra = ';'.join([f"{prod_id}:{qtd}" for prod_id, qtd in self.carrinho.items()])
            self.socket.sendall(f'COMPRAR {compra}'.encode())

            # Atualizar o estoque localmente após a compra
            for prod_id, qtd in self.carrinho.items():
                self.produtos[prod_id]['estoque'] -= qtd

            # Limpar o carrinho após a compra
            self.carrinho.clear()

            # Exibir uma mensagem amigável
            print("Compra finalizada com sucesso! Obrigado por comprar conosco.")
        else:
            print("Compra cancelada.")

if __name__ == '__main__':
    cliente = Cliente()
    cliente.start()
