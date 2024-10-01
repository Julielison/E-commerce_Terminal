from Estruturas.LinearProbingLoadFactor import HashTable
from Estoque.estoque import Estoque

class Protocolo:
    métodos = HashTable()
    
    @classmethod
    def mapear_função(cls, metodo: str) -> any:
        return cls.métodos[metodo][0]
    
    @classmethod
    def obter_código_sucesso(cls, metodo: str) -> any:
        return cls.métodos[metodo][1]
    
    @classmethod
    def obter_código_erro(cls, metodo: str) -> str:
        return cls.métodos[metodo][2]
        
    @classmethod
    def carregar_dados(cls, estoque) -> None:
        
        cls.métodos.put('PEGAR_PRODUTOS', (estoque.pegar_produtos, 'PROD-220'))
        cls.métodos.put('PEGAR_CATEGORIAS', (estoque.pegar_categorias, 'CATE-221'))
        cls.métodos.put('PEGAR_PRODUTOS_DA_CATEGORIA', (estoque.pegar_produtos_da_categoria, 'PRCA-222'))
        cls.métodos.put('COMPRAR', (estoque.comprar_produtos, 'COMP-223'))

    @classmethod
    def montar_mensagem(cls, código_resposta:str, mensagem: str = '', resultado = '') -> str:
        return codigo