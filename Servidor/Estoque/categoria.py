class Categoria:
    def __init__(self, nome: str) -> None:
        self.__nome = nome

    @property
    def nome(self) -> str:
        return self.__nome