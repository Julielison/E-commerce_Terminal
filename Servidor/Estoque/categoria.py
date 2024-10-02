class Categoria:
    """
    Classe que representa uma categoria com um nome.
    
    Atributos:
        __nome (str): Nome da categoria, armazenado como um atributo privado.
    """

    def __init__(self, nome: str) -> None:
        """
        Inicializa uma instância da classe Categoria.
        
        Args:
            nome (str): O nome da categoria.
        """
        self.__nome = nome

    @property
    def nome(self) -> str:
        """
        Retorna o nome da categoria.
        
        Returns:
            str: O nome da categoria.
        """
        return self.__nome