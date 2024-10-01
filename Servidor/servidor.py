import threading
import socket
import time
from protocolo import Protocolo
from Estoque.estoque import Estoque


class Servidor:
    def __init__(self):
        self.host = 'localhost'
        self.port = 55550
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.semaforo = threading.Semaphore(1) 

    def start(self):  # Inicia o servidor
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        print('Servidor executando na porta: ', self.port)
        while True:
            conn, addr = self.socket.accept()
            print('Conectado a', addr)
            threading.Thread(target=self.handle_client, args=(conn,)).start()

    def handle_client(self, conn):  # Trata a conexão com o cliente e executa os comandos recebidos
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

            # Aqui usamos o semáforo para controlar o acesso ao estoque
            with self.semaforo:
                resultado = self.processar_requisição(método, corpo_entidade)

            conn.sendall(resultado.encode())
        conn.close()


    def processar_requisição(self, método: str, corpo_entidade: str) -> str:
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
    estoque = Estoque()
    estoque.preencher()
    Protocolo.carregar_protocolo_padrão(estoque)
    servidor = Servidor()
    servidor.start()
