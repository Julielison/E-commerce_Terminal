import socket
import threading
from tabulate import tabulate

class Cliente:
    """
    Classe Cliente que simula a interação de um usuário com um sistema de e-commerce através de um cliente TCP.
    O cliente se conecta a um servidor, permite visualizar produtos e categorias, adicionar itens ao carrinho e finalizar compras.

    Atributos:
        host (str): Endereço do servidor, por padrão 'localhost'.
        port (int): Porta de comunicação com o servidor.
        socket (socket.socket): Socket utilizado para comunicação.
        nome_cliente (str): Nome do cliente.
        carrinho (dict): Carrinho de compras, armazena os produtos e suas quantidades.
        produtos (dict): Dicionário que armazena os detalhes dos produtos recebidos do servidor.
        running (bool): Sinalizador para controlar a execução da thread de recebimento de mensagens.
    
    Métodos:
        start(): Inicia a conexão com o servidor e exibe o menu de opções ao cliente.
        show_menu(): Exibe o menu de opções disponíveis para o cliente.
        receive_message(): Thread responsável por receber e processar mensagens do servidor.
        adicionar_ao_carrinho(): Adiciona produtos ao carrinho com base no ID e na quantidade informada.
        finalizar_compra(): Finaliza a compra, exibe os itens do carrinho e envia a solicitação de compra ao servidor.
    """

    def __init__(self):
        """
        Inicializa o cliente com os parâmetros de host, porta e configura os atributos para o carrinho de compras
        e produtos disponíveis.
        """
        self.host = 'localhost'
        self.port = 55550
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nome_cliente = None
        self.carrinho = {}
        self.produtos = {}  # Para armazenar os detalhes dos produtos recebidos
        self.running = True  # Sinalizador para a thread de recebimento de mensagens

    def start(self) -> None:
        """
        Inicia a conexão com o servidor e mantém o loop principal do cliente.
        O cliente pode enviar comandos ao servidor e processar as respostas.
        """
        self.socket.connect((self.host, self.port))
        print('Conectado ao servidor')

        # Mensagem de boas-vindas
        self.nome_cliente = input("Bem-vindo ao E-commerce! Por favor, insira seu nome: ")
        print(f"Olá, {self.nome_cliente}! Abaixo estão as opções disponíveis:")

        # Iniciar a thread de recebimento de mensagens do servidor
        threading.Thread(target=self.receive_message, daemon=True).start()

        # Loop principal do cliente
        while True:
            self.show_menu()
            opcao = input("\nEscolha uma opção: ")

            if opcao == '5':  # SAIR
                self.running = False  # Para a thread de recebimento de mensagens
                self.socket.sendall('SAIR'.encode())
                print("Obrigado por usar nosso serviço! Tenha um bom dia!")
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

    def show_menu(self) -> None:
        """
        Exibe o menu de opções que o cliente pode escolher.
        """
        menu = """
        [1] VER PRODUTOS
        [2] VER CATEGORIAS
        [3] ADICIONAR PRODUTO AO CARRINHO
        [4] FINALIZAR COMPRA
        [5] SAIR
        """
        print(menu)

    def receive_message(self) -> None:
        """
        Thread responsável por receber e processar as mensagens do servidor.
        As mensagens podem conter a lista de produtos ou categorias e são exibidas ao cliente.
        """
        while self.running:
            try:
                data = self.socket.recv(1024)
                if not data:  # Verifica se a conexão foi fechada
                    print("Conexão com o servidor encerrada.")
                    break
                resposta = data.decode().split('@#')

                if resposta[0] == 'PROD-220':
                    # Exibir produtos com tabulate
                    produtos = [p.split('#') for p in resposta[1].split('##')]
                    headers = ['ID', 'Nome', 'Preço', 'Quantidade']
                    self.produtos = {prod[0]: {'nome': prod[1], 'preco': float(prod[2]), 'estoque': int(prod[3])} for prod in produtos}
                    print(tabulate(produtos, headers, tablefmt="grid"))

                elif resposta[0] == 'CATE-221':
                    # Exibir categorias com tabulate
                    categorias = resposta[1].split('#')
                    print("\nCategorias disponíveis:")
                    categoria_table = [[categoria] for categoria in categorias if categoria.strip()]
                    print(tabulate(categoria_table, headers=['Categorias'], tablefmt="grid"))

                elif resposta[0] == 'COMP-223':
                    # Tratamento da mensagem de confirmação de compra
                    print("\nCompra confirmada pelo servidor. Obrigado por usar nosso serviço!\n")

                else:
                    print(f"Resposta não reconhecida: {resposta[0]}")
            except Exception as e:
                print("Erro ao receber mensagem do servidor:", str(e))
                break

    def adicionar_ao_carrinho(self) -> None:
        """
        Adiciona um produto ao carrinho de compras com base no ID e na quantidade informados pelo cliente.
        Verifica se o ID é válido e se a quantidade solicitada está disponível em estoque.
        """
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
        except ValueError:
            print("Por favor, insira uma quantidade válida.")
        except Exception as e:
            print("Erro ao adicionar produto ao carrinho:", str(e))

    def finalizar_compra(self) -> None:
        """
        Exibe os itens do carrinho de compras e o total da compra.
        Permite ao cliente confirmar a finalização da compra e envia o pedido ao servidor.
        """
        if not self.carrinho:
            print("Seu carrinho está vazio!")
            return

        # Exibir os itens do carrinho
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
            try:
                # Enviar os detalhes da compra ao servidor
                compra = ';'.join([f"{prod_id}:{qtd}" for prod_id, qtd in self.carrinho.items()])
                self.socket.sendall(f'COMPRAR {compra}'.encode())

                # Atualizar o estoque localmente
                for prod_id, qtd in self.carrinho.items():
                    self.produtos[prod_id]['estoque'] -= qtd

                self.carrinho.clear()
                print("Compra finalizada com sucesso!")
            except Exception as e:
                print("Erro ao finalizar a compra:", str(e))
        else:
            print("Compra cancelada.")

if __name__ == '__main__':
    cliente = Cliente()
    cliente.start()
