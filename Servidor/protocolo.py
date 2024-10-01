from Estruturas.LinearProbingLoadFactor import HashTable
from Estoque.estoque import Estoque

class Protocolo:
    métodos = HashTable()
    código_resposta = ''
    
    @classmethod
    def mapear_função(cls, metodo: str):
        return cls.métodos[metodo]
        
    @classmethod
    def criar(cls, estoque) -> None:
        cls.métodos.put('PEGAR_PRODUTOS', estoque.pegar_produtos)
        cls.métodos.put('PEGAR_CATEGORIAS', estoque.pegar_categorias)
        cls.métodos.put('PEGAR_PRODUTOS_DA_CATEGORIA', estoque.pegar_produtos_da_categoria)
        cls.métodos.put('COMPRAR', estoque.comprar_produtos)

    @classmethod
    def montar_mensagem(cls, código_resposta:str,)