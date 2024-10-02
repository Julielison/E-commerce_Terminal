import re
from .categoria import Categoria
from .sql import Sql
from Estruturas.LinearProbingLoadFactor import HashTable
from Estruturas.listaEncadeada import Lista
from Estoque.produto import Produto
import sqlite3


class Estoque:
    qtd_produtos = 0
    qtd_categorias = 0

    def __init__(self):
        self.estoque = HashTable()
        self.categorias = Lista()

    def preencher(self) -> None:
        # Conectar ao banco de dados SQLite
        conn = sqlite3.connect('Servidor\Estoque\data_base.db')
        cursor = conn.cursor()
        comando = Sql.categorias()

        # Executar um SELECT para pegar todos os nomes das categorias
        cursor.execute(comando)

        # Recuperar os resultados
        categorias = cursor.fetchall()

        i = 1
        for cat in categorias:
            categoria = Categoria(str(cat[0]))
            self.categorias.inserir(i, categoria)
            i += 1
            Estoque.qtd_categorias += 1

            comando = Sql.produtos_por_categoria()

            # Executar um SELECT para pegar produtos dessa categoria
            cursor.execute(comando, (categoria.nome,))

            # Recuperar os produtos da categoria
            produtos = cursor.fetchall()

            # Preencher o estoque com os produtos
            for prod in produtos:
                id = prod[0]
                nome = prod[1]
                preço = prod[2]
                qtd = prod[3]
                produto = Produto(nome, float(preço), int(qtd), categoria)
                self.estoque.put(id, produto)
                Estoque.qtd_produtos += 1

        # Fechar a conexão
        conn.close()


    def pegar_categorias(self) -> str:
        resultado = ''
        for i in range(1, Estoque.qtd_categorias+1):
            resultado += f'{self.categorias.elemento(i).nome}#'

        return resultado.rstrip('#')
            

    def pegar_produtos(self, id_inicio = 0) -> str:
        id_inicio = int(id_inicio)
        qtd = Estoque.qtd_produtos
        total = 5

        if id_inicio+total > qtd:
            raise Exception('Sem_produtos_para_exibir.')
        
        resultado = ''
        cont = 0
        while cont < total and id_inicio <= qtd:
                id_inicio += 1
                try:
                    produto = self.estoque.get(id_inicio)
                except:
                    continue
                resultado += self.__montar_string_produto(id_inicio, produto)
                cont += 1
        
        return resultado.rstrip('##')

    
    def pegar_produtos_da_categoria(self, categoria: str) -> str:
        resultado = ''
        cont = 0
        for id, produto in self.estoque.items():
            if produto.categoria == categoria:
                resultado += self.__montar_string_produto(id, produto)
                cont +=1
                if cont == 10:
                    break

        if resultado == '':
            raise Exception("Sem_produtos_para_essa_categoria")
        
        return resultado.rstrip('##')


    def pesquisar_produto(self, nome: str) -> str:
        padrao = re.compile(rf'\b{re.escape(nome)}\b', re.IGNORECASE)
        resultado = ''
    
        # Verificar se há uma correspondência
        cont = 0
        for id in self.estoque.keys():
            try:
                produto = self.estoque.get(id)
            except:
                continue
            if padrao.search(produto.nome):
                resultado += self.__montar_string_produto(id, produto)
                cont += 1
            if cont == 10:
                break
        
        if resultado == '':
            raise Exception('Nenhum produto encontrado.')

        return resultado.rstrip('##')

    def __montar_string_produto(self, id: str, produto: Produto) -> str:
        return f'{id}#{produto.nome}#{produto.preco}#{produto.quantidade}##'


    def comprar(self, dados: str) -> str:
        '''
        '''
        resultado = ''
        flag = False

        prod_qtd = dados

        if ';' in prod_qtd:
            prod_qtd = prod_qtd.split(';')

            for e in prod_qtd:
                id, qtd = e.split(':')
                id = int(id)
                qtd = int(qtd)  # Converter qtd para inteiro
                try:
                    produto = self.estoque.get(id)
                except:
                    resultado += f'{id}#{0}##'
                    continue

                if qtd > produto.quantidade:
                    resultado += f'{id}#{produto.quantidade}##'
                    flag = True
                else:
                    produto.quantidade -= qtd  # Subtrai a quantidade comprada
                    if produto.quantidade == 0:
                        self.estoque.remove(id)

        else:
            id, qtd = prod_qtd.split(':')
            id = int(id)
            qtd = int(qtd)  # Converter qtd para inteiro
            try:
                produto = self.estoque.get(id)
            except:
                flag = True
                resultado += f'{id}#{0}##'
                produto = None  # Garantir que produto não será acessado abaixo se a exceção ocorrer

            if produto is not None:  # Certificar que o produto foi encontrado
                if qtd > produto.quantidade:
                    resultado += f'{id}#{produto.quantidade}##'
                    flag = True
                else:
                    produto.quantidade -= qtd  # Subtrai a quantidade comprada
                    if produto.quantidade == 0:
                        self.estoque.remove(id)

        if flag:
            raise Exception('Quantidade_ou_produto_indisponível ' + resultado.rstrip('##'))

        return 'Compra finalizada'
