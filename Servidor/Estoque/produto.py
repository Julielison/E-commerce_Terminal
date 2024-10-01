from Servidor.Estruturas.listaEncadeada import Lista
from categoria import Categoria

'''
Classe usada para criar um objeto produto.
'''
class Produto:
    def __init__(self, nome: str, preco: float, quantidade: int, categoria: Categoria) -> None:
        self.__nome = nome
        self.__preco = preco
        self.__quantidade = quantidade
        self.__categoria = categoria


    # Propriedade para nome
    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str) -> None:
        if not isinstance(nome, str):
            raise TypeError('O nome deve ser uma string')
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


    @property
    def categoria(self) -> str:
        return self.__categoria.nome