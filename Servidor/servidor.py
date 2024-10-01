import threading
import socket
from protocolo import Protocolo


class Servidor:
    def __init__(self):
        self.host = 'localhost'
        self.port = 55550
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def start (self): # Inicia o servidor
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        print('Servidor executando na porta: ', self.port)
        while True:
            conn, addr = self.socket.accept()
            print('Conectado a', addr)
            threading.Thread(target=self.handle_client, args=(conn,)).start()
            

    def handle_client(self, conn): # Trata a conexão com o cliente e executa os comandos recebidos do cliente(Cria uma thread para cada cliente)

        while True:
            data = conn.recv(1024)
            data = data.decode()
            print('Recebido:', data)

            entidade = None
            dados_separados = data.split()
            método = dados_separados[0]
        
            if len(dados_separados) > 1:
                entidade = dados_separados[1]

            if método == 'SAIR':
                break

            try:
                processar_no_estoque = Protocolo.mapear_função(método)
                if entidade != None:
                    resultado = processar_no_estoque(entidade)
                else:
                    resultado = processar_no_estoque()
            except Exception as e:
                pass

            conn.sendall(resultado)
        conn.close()


if __name__ == '__main__':
    servidor = Servidor()
    servidor.start()