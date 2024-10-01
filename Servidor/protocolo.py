import csv
from Estruturas.LinearProbingLoadFactor import HashTable


class Protocolo:
    métodos = HashTable()
    
    @classmethod
    def mapear_função(cls, metodo: str) -> any:
        try:
            return cls.métodos[metodo][0]
        except:
            raise Exception('ERRO-305@#Método não encontrado.')
    
    @classmethod
    def carregar_protocolo_padrão(cls, objeto) -> None:
        with open('Servidor/protocolo.csv', mode='r', encoding='utf-8') as arquivo:
            leitor_csv = csv.reader(arquivo)
            
            # Pular o cabeçalho
            next(leitor_csv)
            
            # Iterar pelas linhas do arquivo
            for linha in leitor_csv:
                print(linha)
                metodo, codigo_sucesso, codigo_erro = linha
                método_estoque = getattr(objeto, metodo.lower())
                cls.métodos[metodo] = (método_estoque, codigo_sucesso, codigo_erro)

    @classmethod
    def montar_resposta_sucesso(cls, método:str, resultado: str) -> str:
        return cls.métodos[método][1] + '@#' + resultado
    
    @classmethod
    def montar_resposta_erro(cls, método:str, mensagem: str) -> str:
        print(método)
        return cls.métodos[método][2] + '@#' +  mensagem