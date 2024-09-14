from produto import Produto

# Armazena os produtos por categoria
class Estoque:
    def __init__(self) -> None:
        self.__estoque = {}

    def adicionar_categoria_estoque(self) -> dict: #Adiciona uma categoria ao estoque
        categoria = input("Digite a categoria que deseja adicionar ao estoque: ")
        self.__adicionarCategoriaEstoque(categoria)
        return self.estoque
    

    def adicionarProdutoEstoque(self) -> dict: #Adiciona um produto a uma categoria do estoque
        categoria = input("Digite a categoria do produto: ")
        produto = input("Digite o nome do produto: ")
        preco = float(input("Digite o preco do produto: "))
        quantidade = int(input("Digite a quantidade do produto: "))
        self.__adicionarProdutoEstoque(categoria, produto, preco, quantidade)
        return self.estoque
    
    def removerProdutoEstoque(self) -> dict: #Remove um produto de uma categoria do estoque
        categoria = input("Digite a categoria do produto que deseja remover: ")
        produto = input("Digite o nome do produto que deseja remover: ")
        self.removerProdutoEstoque(categoria, produto)
        return self.estoque
    
    
    def __createList(self, categoria:str) -> list: #Cria uma lista vazia para uma categoria do estoque
        self.estoque[categoria] = list()
        return self.estoque[categoria]
    
    def __adicionarCategoriaEstoque(self, categoria:list ) -> list :  #Adiciona uma categoria ao estoque 
        listCategoria = self.__createList(categoria)
        self.estoque[categoria] = listCategoria
        return self.estoque
    
    def __adicionarProdutoEstoque(self, categoria:str, produto:str, preco:float, quantidade:int) -> dict: #Adiciona um produto a uma categoria do estoque(Corrigir)        
        self.estoque[categoria] = {"produto":produto, "preco":preco, "quantidade":quantidade} # Consertar essa linha (não está adicionando o produto mais de um produto)
  
        return self.estoque
    
    def removerProdutoEstoque(self, categoria:str, produto:str) -> dict: #Remove um produto de uma categoria do estoque
        categoria = input("Digite a categoria do produto que deseja remover: ")
        produto = input("Digite o nome do produto que deseja remover: ")
        del self.estoque[categoria][produto]
        return self.estoque
    
    def listarEstoque(self) -> dict: #Lista o estoque
        print(self.estoque)
        return self.estoque
    

    def interface(self) -> None:
        threading.Thread(target=self.__interfaceEstoque).start()
        return None

    
    def __interfaceEstoque(self) -> None:
        print(f"Bem vindo ao sistema de estoque ")
        print(f" Selecione a opção desejada")
        print("1 - Adicionar categoria ao estoque")
        print("2 - Adicionar produto ao estoque")
        print("3 - Remover produto do estoque")
        print("4 - Listar estoque")
        print("5 - Sair")

        options = {'1':self.adicionarCategoriaEstoque, '2':self.adicionarProdutoEstoque, '3':self.removerProdutoEstoque, '4':self.listarEstoque, '5':sys.exit}
        
        while True:
            option = input("Digite a opcao desejada: ")
            if option in options:
                options[option]()
            else:
                print("Opção inválida. Tente novamente.")
            
            if option == '5':
                break
        return None