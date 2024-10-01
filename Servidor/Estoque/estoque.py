from Servidor.Estoque.categoria import Categoria
from Servidor.Estoque.sql import Sql
from Servidor.Estruturas.LinearProbingLoadFactor import HashTable
from Servidor.Estruturas.listaEncadeada import Lista
from Servidor.Estoque.produto import Produto
import csv
import sqlite3




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
        string = ''
        for cat in self.categorias:
            string += cat.nome
        return string
            

    def pegar_produtos(self, inicio = 1) -> str:
        qtd = Estoque.qtd_produtos

        if inicio > qtd:
            raise Exception('Sem mais produtos')
        string = ''

        for i in range(inicio, qtd+1):
            try:
                self.estoque.get()

    def comprar_produtos(self, dados: str) -> str:
        '''
        Formato dos dados: categoria;id.quantidade;id.quantidade,categoria;id.quantidade ...
        '''
        resultado = ''
        esgotados = []
        limitados = {}
        comprados = {}
        
        # Processar os dados (exemplo de como eles podem ser divididos)
        categorias_dados = dados.split(',')
        for categoria_dados in categorias_dados:
            categoria, *ids_e_qtds = categoria_dados.split(';')
            for id_qtd in ids_e_qtds:
                id, qtd = map(int, id_qtd.split('.'))
                produto = self.obter_produto(categoria, id)  # Obter produto pelo id e categoria

                if produto.quantidade == 0:
                    esgotados.append(id)
                elif produto.quantidade < qtd:
                    limitados[id] = produto.quantidade
                else:
                    produto.quantidade -= qtd  # Reduzir a quantidade
                    comprados[id] = qtd  # Registrar o produto comprado

        resposta = {'comprados': comprados, 'limitados': limitados, 'esgotados': esgotados}
        return json.dumps(resposta)

    def obter_produto(self, categoria: str, id: int) -> Produto:
        """ Método para obter um produto específico dado a categoria e o ID. """
        return self.estoque[categoria][id]