from Servidor.Estruturas.LinearProbingLoadFactor import HashTable
from Servidor.Estoque.produto import Produto
import csv

class Estoque:
    estoque = HashTable()

    @classmethod
    def carregar_estoque(cls) -> None:
        cls.adicionar_categorias('Categorias.csv')
        cls.adicionar_produtos()

    @classmethod
    def adicionar_categorias(cls, arquivo: str) -> None:
        try:
            with open(f'./Csv{arquivo}', mode='r', newline='', encoding='utf-8') as arquivo_csv:
                leitor = csv.reader(arquivo_csv)
                next(leitor)
                
                # Ler cada linha do arquivo
                for categoria in leitor:
                    cls.estoque[categoria] = HashTable()

        except FileNotFoundError:
            print(f"O arquivo '{arquivo}' não foi encontrado.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")


    @classmethod
    def adicionar_produtos(cls) -> None:
        for categoria in cls.estoque.keys():
            try:
                with open(f'./Csv{categoria}.csv', mode='r', newline='', encoding='utf-8') as arquivo_csv:
                    leitor = csv.reader(arquivo_csv)
                    next(leitor)
                    
                    id = 1
                    for linha in leitor:
                        nome, preço, quantidade = linha[0], linha[1], linha[2]
                        cls.estoque[categoria][id] = HashTable(Produto(nome, preço, quantidade))
                        id += 1

            except FileNotFoundError:
                print(f"O arquivo da categoria {categoria} não foi encontrado.")
            except Exception as e:
                print(f"Ocorreu um erro: {e}")

    @classmethod
    def pegar_categorias(cls) -> list:
        return cls.estoque.keys()
    
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