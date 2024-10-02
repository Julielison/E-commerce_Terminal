import threading
import socket
from protocolo import Protocolo
from Estoque.estoque import Estoque


class Servidor:
    """
    Classe Servidor que implementa um servidor TCP multi-thread para processar requisições de um cliente
    e interagir com o estoque de produtos.

    Atributos:
        host (str): Endereço do servidor, por padrão 'localhost'.
        port (int): Porta na qual o servidor irá ouvir as conexões.
        socket (socket.socket): Socket utilizado para estabelecer conexões.
        semaforo (threading.Semaphore): Semáforo utilizado para controlar o acesso ao estoque compartilhado entre threads.

    Métodos:
        start(): Inicia o servidor e aguarda por conexões de clientes.
        handle_client(conn): Manipula a comunicação com o cliente e processa as requisições recebidas.
        processar_requisição(método, corpo_entidade): Processa a requisição enviada pelo cliente e retorna a resposta.
    """

    def __init__(self):
        """
        Inicializa o servidor com os parâmetros de host, porta e configura o semáforo para controle de threads.
        """
        self.host = 'localhost'
        self.port = 55550
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.semaforo = threading.Semaphore(1)

    def start(self) -> None:
        """
        Inicia o servidor, vincula o socket ao endereço e porta, e aguarda por conexões de clientes.
        Ao receber uma conexão, inicia uma nova thread para lidar com o cliente.
        """
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        print('Servidor executando na porta:', self.port)
        while True:
            conn, addr = self.socket.accept()
            print('Conectado a', addr)
            threading.Thread(target=self.handle_client, args=(conn,)).start()

    def handle_client(self, conn: socket.socket) -> None:
        """
        Manipula a comunicação com o cliente, recebendo dados, processando a requisição e enviando a resposta.
        Usa um semáforo para controlar o acesso ao estoque durante o processamento das requisições.

        Args:
            conn (socket.socket): Conexão com o cliente.
        """
        while True:
            data = conn.recv(1024)
            data = data.decode()
            print('Recebido:', data)

            corpo_entidade = None
            dados_separados = data.split()
            método = dados_separados[0]

            if len(dados_separados) > 1:
                corpo_entidade = dados_separados[1]

            if método == 'SAIR':
                break

            # Controle de acesso ao estoque usando o semáforo
            with self.semaforo:
                resultado = self.processar_requisição(método, corpo_entidade)

            conn.sendall(resultado.encode())
        conn.close()

    def processar_requisição(self, método: str, corpo_entidade: str) -> str:
        """
        Processa a requisição recebida pelo cliente, mapeia o método solicitado para uma função correspondente
        e retorna a resposta apropriada (sucesso ou erro).

        Args:
            método (str): O nome do método solicitado.
            corpo_entidade (str): Parâmetro adicional enviado na requisição.

        Returns:
            str: A resposta da operação, incluindo códigos de sucesso ou erro.
        """
        try:
            processar_no_estoque = Protocolo.mapear_função(método)
        except Exception as msg:
            return str(msg)

        try:
            if corpo_entidade is not None:
                resultado = processar_no_estoque(corpo_entidade)
            else:
                resultado = processar_no_estoque()
            resultado = Protocolo.montar_resposta_sucesso(método, resultado)
        except Exception as mensagem:
            resultado = Protocolo.montar_resposta_erro(método, str(mensagem))

        return resultado


if __name__ == '__main__':
    """
    Código principal que inicializa o estoque, carrega o protocolo e inicia o servidor.
    """
    estoque = Estoque()
    estoque.preencher()
    Protocolo.carregar_protocolo_padrão(estoque)
    servidor = Servidor()
    servidor.start()