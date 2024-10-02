from .categoria import Categoria

'''
Classe usada para criar um objeto produto com atributos como nome, preço, quantidade e categoria.
'''
class Produto:
    def __init__(self, nome: str, preco: float, quantidade: int, categoria: Categoria) -> None:
        """
        Inicializa uma instância da classe Produto.

        Args:
            nome (str): O nome do produto.
            preco (float): O preço do produto.
            quantidade (int): A quantidade em estoque do produto.
            categoria (Categoria): A categoria do produto.
        """
        self.__nome = nome
        self.__preco = preco
        self.__quantidade = quantidade
        self.__categoria = categoria

    # Propriedade para nome
    @property
    def nome(self) -> str:
        """
        Retorna o nome do produto.

        Returns:
            str: O nome do produto.
        """
        return self.__nome

    @nome.setter
    def nome(self, nome: str) -> None:
        """
        Define o nome do produto após validar que é uma string e possui no mínimo 2 caracteres.

        Args:
            nome (str): O novo nome do produto.

        Raises:
            TypeError: Se o nome não for uma string.
            ValueError: Se o nome tiver menos de 2 caracteres.
        """
        if not isinstance(nome, str):
            raise TypeError('O nome deve ser uma string')
        if len(nome) < 2:
            raise ValueError('O nome do produto deve ter no mínimo 2 caracteres')
        self.__nome = nome

    # Propriedade para preço
    @property
    def preco(self) -> float:
        """
        Retorna o preço do produto.

        Returns:
            float: O preço do produto.
        """
        return self.__preco

    @preco.setter
    def preco(self, preco: float) -> None:
        """
        Define o preço do produto, garantindo que não seja um valor negativo.

        Args:
            preco (float): O novo preço do produto.

        Raises:
            ValueError: Se o preço for negativo.
        """
        if preco < 0:
            raise ValueError('O preço não pode ser negativo')
        self.__preco = preco

    # Propriedade para quantidade
    @property
    def quantidade(self) -> int:
        """
        Retorna a quantidade em estoque do produto.

        Returns:
            int: A quantidade do produto.
        """
        return self.__quantidade

    @quantidade.setter
    def quantidade(self, quantidade: int) -> None:
        """
        Define a quantidade do produto, garantindo que não seja um valor negativo.

        Args:
            quantidade (int): A nova quantidade do produto.

        Raises:
            ValueError: Se a quantidade for negativa.
        """
        if quantidade < 0:
            raise ValueError('A quantidade não pode ser negativa')
        self.__quantidade = quantidade

    @property
    def categoria(self) -> str:
        """
        Retorna o nome da categoria do produto.

        Returns:
            str: O nome da categoria do produto.
        """
        return self.__categoria.nome