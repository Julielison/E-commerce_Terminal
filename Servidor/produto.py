'''
Classe usada para criar um objeto produto.
'''
class Produto:
    def __init__(self, nome: str, preco: float, quantidade: int) -> None:
        self.__nome = nome
        self.__preco = preco
        self.__quantidade = quantidade

    # Propriedade para nome
    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str) -> None:
        if len(nome) < 2:
            raise ValueError('O nome do produto deve ter no mínimo 2 caracteres')
        self.__nome = nome

    # Propriedade para preço
    @property
    def preco(self) -> float:
        return self.__preco

    @preco.setter
    def preco(self, preco: float) -> None:
        if preco < 0:
            raise ValueError('O preço não pode ser negativo')
        self.__preco = preco

    # Propriedade para quantidade
    @property
    def quantidade(self) -> int:
        return self.__quantidade

    @quantidade.setter
    def quantidade(self, quantidade: int) -> None:
        if quantidade < 0:
            raise ValueError('A quantidade não pode ser negativa')
        self.__quantidade = quantidade

'''
A classe abaixo visa otimizar a obtenção dos dados de um produto quando o cliente efetua uma compra.
'''
class Produtos:
    __produtos = {}
    __contador = 0

    @classmethod
    def exibir_produtos(cls) -> dict:
        return cls.__produtos
    
    @classmethod
    def adicionar_produto(cls, produto: Produto) -> None:
        cls.__produtos[cls.__contador+1] = produto

    @classmethod
    def obter_produto(cls, id: int) -> any:
        return cls[id]