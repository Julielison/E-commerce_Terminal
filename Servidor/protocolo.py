import csv
from Estruturas.LinearProbingLoadFactor import HashTable


class Protocolo:
    """
    Classe Protocolo que gerencia a associação de métodos com seus códigos de sucesso e erro.
    Ela permite carregar os protocolos de um arquivo CSV e mapear métodos para tratamento
    de respostas de sucesso ou erro.

    Atributos:
        métodos (HashTable): Tabela de hash que armazena os métodos mapeados com seus respectivos
                             códigos de sucesso e erro.
    """
    
    métodos = HashTable()
    
    @classmethod
    def mapear_função(cls, metodo: str) -> any:
        """
        Mapeia e retorna a função associada ao método fornecido.

        Args:
            metodo (str): O nome do método a ser mapeado.

        Returns:
            any: Função associada ao método.

        Raises:
            Exception: Se o método não for encontrado na tabela.
        """
        try:
            return cls.métodos[metodo][0]
        except:
            raise Exception('ERRO-305@#Método não encontrado.')
    
    @classmethod
    def carregar_protocolo_padrão(cls, objeto) -> None:
        """
        Carrega os protocolos padrões a partir de um arquivo CSV e mapeia os métodos
        do objeto fornecido para serem utilizados pelo protocolo.

        Args:
            objeto (any): O objeto que contém os métodos a serem mapeados.
        """
        with open('Servidor/protocolo.csv', mode='r', encoding='utf-8') as arquivo:
            leitor_csv = csv.reader(arquivo)
            
            # Pular o cabeçalho
            next(leitor_csv)
            
            # Iterar pelas linhas do arquivo
            for linha in leitor_csv:
                metodo, codigo_sucesso, codigo_erro = linha
                método_estoque = getattr(objeto, metodo.lower())
                cls.métodos[metodo] = (método_estoque, codigo_sucesso, codigo_erro)

    @classmethod
    def montar_resposta_sucesso(cls, método: str, resultado: str) -> str:
        """
        Monta uma string de resposta de sucesso com base no método e no resultado fornecidos.

        Args:
            método (str): O nome do método utilizado.
            resultado (str): O resultado da operação.

        Returns:
            str: Resposta formatada com o código de sucesso e o resultado concatenados.
        """
        return cls.métodos[método][1] + '@#' + resultado
    
    @classmethod
    def montar_resposta_erro(cls, método: str, mensagem: str) -> str:
        """
        Monta uma string de resposta de erro com base no método e na mensagem fornecidos.

        Args:
            método (str): O nome do método utilizado.
            mensagem (str): A mensagem de erro.

        Returns:
            str: Resposta formatada com o código de erro e a mensagem concatenados.
        """
        return cls.métodos[método][2] + '@#' + mensagem