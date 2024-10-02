import re
from .categoria import Categoria
from .sql import Sql
from Estruturas.LinearProbingLoadFactor import HashTable
from Estruturas.listaEncadeada import Lista
from Estoque.produto import Produto
import sqlite3


class Estoque:
    """
    Classe que representa o estoque de uma loja, contendo produtos e categorias.

    Atributos:
        qtd_produtos (int): Quantidade total de produtos no estoque.
        qtd_categprias (int): Quantidade total de categorias no estoque.
    """

    qtd_produtos = 0
    qtd_categprias = 0

    def __init__(self) -> None:
        """
        Inicializa uma instância da classe Estoque.

        Cria uma hash table para armazenar os produtos e uma lista encadeada para as categorias.
        """
        self.estoque = HashTable()
        self.categorias = Lista()

    def preencher(self) -> None:
        """
        Preenche o estoque e categorias com dados vindos de um banco de dados SQLite.

        Realiza consultas SQL para obter categorias e seus respectivos produtos, e insere
        esses dados na tabela de hash e na lista de categorias.
        """
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
            Estoque.qtd_categprias += 1

            comando = Sql.produtos_por_categoria()

            # Executar um SELECT para pegar produtos dessa categoria
            cursor.execute(comando, (categoria.nome,))

            # Recuperar os produtos da categoria
            produtos = cursor.fetchall()

            # Preencher o estoque com os produtos
            for prod in produtos:
                id = prod[0]
                nome = prod[1]
                preco = prod[2]
                qtd = prod[3]
                produto = Produto(nome, float(preco), int(qtd), categoria)
                self.estoque.put(id, produto)
                Estoque.qtd_produtos += 1

        # Fechar a conexão
        conn.close()

    def pegar_categorias(self) -> str:
        """
        Retorna uma string contendo todas as categorias do estoque separadas por '#'.

        Returns:
            str: Categorias do estoque separadas por '#'.
        """
        resultado = ''
        for i in range(1, Estoque.qtd_categprias + 1):
            resultado += f'{self.categorias.elemento(i).nome}#'

        return resultado.rstrip('#')

    def pegar_produtos(self, id_inicio=0) -> str:
        """
        Retorna uma lista de produtos a partir de um ID inicial, limitando a 10 produtos.

        Args:
            id_inicio (int): ID inicial do produto para iniciar a busca.

        Returns:
            str: Produtos no formato 'id#nome#preco#quantidade##'.
        
        Raises:
            Exception: Se não houver produtos suficientes para exibir.
        """
        id_inicio = int(id_inicio)
        qtd = Estoque.qtd_produtos
        total = 10

        if id_inicio + total > qtd:
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
        """
        Retorna uma string com todos os produtos de uma categoria específica.

        Args:
            categoria (str): Nome da categoria.

        Returns:
            str: Produtos da categoria no formato 'id#nome#preco#quantidade##'.
        
        Raises:
            Exception: Se não houver produtos para a categoria especificada.
        """
        resultado = ''
        for id, produto in self.estoque.items():
            if produto.categoria == categoria:
                resultado += self.__montar_string_produto(id, produto)

        if resultado == '':
            raise Exception("Sem_produtos_para_essa_categoria")
        
        return resultado.rstrip('##')

    def pesquisar_produto(self, nome: str) -> str:
        """
        Pesquisa produtos pelo nome utilizando expressões regulares.

        Args:
            nome (str): Nome do produto a ser pesquisado.

        Returns:
            str: Produtos encontrados no formato 'id#nome#preco#quantidade##'.
        
        Raises:
            Exception: Se nenhum produto for encontrado.
        """
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
        
        if resultado == '':
            raise Exception('Nenhum produto encontrado.')

        return resultado.rstrip('##')

    def __montar_string_produto(self, id: str, produto: Produto) -> str:
        """
        Monta uma string formatada para representar um produto.

        Args:
            id (str): ID do produto.
            produto (Produto): Instância do produto.

        Returns:
            str: String formatada no formato 'id#nome#preco#quantidade##'.
        """
        return f'{id}#{produto.nome}#{produto.preco}#{produto.quantidade}##'

    def comprar(self, dados: str) -> str:
        """
        Realiza a compra de produtos, atualizando a quantidade disponível no estoque.

        Args:
            dados (str): Informações dos produtos a serem comprados no formato 'id:quantidade'.

        Returns:
            str: Confirmação da compra ou exceção caso a quantidade não esteja disponível.

        Raises:
            Exception: Se o produto ou a quantidade estiver indisponível.
        """
        resultado = ''
        flag = False

        prod_qtd = dados

        if ';' in prod_qtd:
            prod_qtd = prod_qtd.split(';')

            for e in prod_qtd:
                id, qtd = e.split(':')
                id = int(id)
                qtd = int(qtd)
                try:
                    produto = self.estoque.get(id)
                except:
                    resultado += f'{id}#{0}##'
                    continue

                if qtd > produto.quantidade:
                    resultado += f'{id}#{produto.quantidade}##'
                    flag = True
                else:
                    produto.quantidade -= qtd
                    if produto.quantidade == 0:
                        self.estoque.remove(id)

        else:
            id, qtd = prod_qtd.split(':')
            id = int(id)
            qtd = int(qtd)
            try:
                produto = self.estoque.get(id)
            except:
                flag = True
                resultado += f'{id}#{0}##'
                produto = None

            if produto is not None:
                if qtd > produto.quantidade:
                    resultado += f'{id}#{produto.quantidade}##'
                    flag = True
                else:
                    produto.quantidade -= qtd
                    if produto.quantidade == 0:
                        self.estoque.remove(id)

        if flag:
            raise Exception('Quantidade_ou_produto_indisponível ' + resultado.rstrip('##'))

        return 'Compra finalizada'