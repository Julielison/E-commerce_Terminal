from Servidor.Estruturas.listaEncadeada import Lista

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



'''
A classe abaixo visa otimizar a obtenção dos dados de um produto quando o cliente envia uma requisição de compra.
'''
class Produtos:
    __produtos = {} # Implementar na HashTable fornecida pelo professor
    __contador = 0

    @classmethod
    def obter_produtos(cls) -> dict:
        return cls.__produtos
    
    @classmethod
    def adicionar_produto(cls, produto: Produto) -> None:
        cls.__produtos[cls.__contador+1] = produto

    @classmethod
    def obter_produto(cls, id: int) -> any:
        try:
            return cls[id]
        except KeyError:
            print(f'O produto com id {id} não está mais disponível.')


    '''
    Cenários:
        quantidade fornecida maior que o disponível
        produto indisponível
    '''
    @classmethod
    def comprar_produtos(cls, ids_qtds: json) -> str:
        ids_e_qtds = json.loads(ids_qtds)
        comprados = Lista()
        esgotados = Lista()
        limitados = {} # Implementar com hashtable fornecida

        for id, qtd in ids_e_qtds.items():
            produto = cls.obter_produto(id)

            if produto.quantidade == 0:
                esgotados.append(id)

            elif produto.quantidade < qtd:
                limitados[id] = produto.quantidade

            else:
                produto.quantidade -= 1
                comprados.append(id)
        
        resposta = {'comprados': comprados, 'limitados': limitados, 'esgotados': esgotados}
        return json.dumps(resposta)