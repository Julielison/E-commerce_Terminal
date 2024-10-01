import re
from Servidor.Estoque.categoria import Categoria
from Servidor.Estoque.sql import Sql
from Servidor.Estruturas.LinearProbingLoadFactor import HashTable
from Servidor.Estruturas.listaEncadeada import Lista
from Servidor.Estoque.produto import Produto
import csv
import sqlite3

class EstoqueErro(Exception):
    """Exceção personalizada para erros específicos na aplicação."""
    
    def __init__(self, mensagem: str):
        super().__init__(mensagem)
        self.mensagem = mensagem


class Estoque:
    qtd_produtos = 0
    def __init__(self):
        self.estoque = HashTable()
        self.categorias = Lista()

    def preencher(self) -> None:
        # Conectar ao banco de dados SQLite
        conn = sqlite3.connect('./data_base.db')
        cursor = conn.cursor()

        comando = Sql.categorias()

        # Executar um SELECT para pegar todos os nomes das categorias
        cursor.execute(comando)

        # Recuperar os resultados
        categorias = cursor.fetchall()

        for cat in categorias:
            categoria = Categoria(cat[0])
            self.categorias.inserir(categoria)  # Adicionar a categoria à lista

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
                produto = Produto(nome, preço, qtd, categoria)
                self.estoque.put(id, produto)
                Estoque.qtd_produtos += 1

        # Fechar a conexão
        conn.close()


    def pegar_categorias(self) -> str:
        resultado = ''
        for cat in self.categorias:
            resultado += f'{cat.nome},'
        return resultado.rtrip(',')
            

    def pegar_produtos(self, id_inicio = 1) -> str:
        qtd = Estoque.qtd_produtos
        total = 10

        if id_inicio+total > qtd:
            raise Exception('Sem_produtos_para_exibir.')
        
        resultado = ''
        cont = 0
        while cont <= total and id_inicio <= qtd:
                try:
                    produto = self.estoque.get(id_inicio)
                except:
                    id_inicio += 1
                    continue
                resultado += self.__montar_string_produto(id_inicio, produto)
                cont += 1
        
        return resultado.rstrip(',')

    
    def pegar_produtos_da_categoria(self, categoria: str) -> str:
        resultado = ''
        for produto in self.estoque.values():
            if produto.categoria == categoria:
                resultado += self.__montar_string_produto(produto)

        if resultado == '':
            raise Exception("Sem_produtos_para_essa_categoria")
        
        return resultado.rstrip(',')


    def pesquisar_produto(self, nome: str) -> str:
        padrao = re.compile(rf'\b{re.escape(nome)}\b', re.IGNORECASE)
        resultado = ''
    
        # Verificar se há uma correspondência
        for id in self.estoque.keys():
            try:
                produto = self.estoque.get(id)
            except:
                continue
            if padrao.search(produto.nome):
                resultado += self.__montar_string_produto(id, produto)

        return resultado.rstrip(',')

    def __montar_string_produto(self, id: str, produto: Produto) -> str:
        return f'{id}:{produto.nome}.{produto.preco}.{produto.quantidade},'


    def comprar_produtos(self, dados: str) -> str:
        '''
            id_produto:quant,id_produto,quant
        '''
        resultado = ''
        flag = False

        prod_qtd = dados.split(',')
        for e in prod_qtd:
            id, qtd = e.split(':'),
            try:
                produto = self.estoque.get(id)
            except:
                flag = True
                continue

            if qtd > produto.quantidade:
                resultado += f'{id}:{qtd},'
                flag = True

            produto.quantidade -= 1
            if produto.quantidade == 0:
                self.estoque.remove(id)
        
        if flag:
            raise Exception('Quantidade_ou_produto_indisponível ' + resultado)

        return resultado.rstrip(',')