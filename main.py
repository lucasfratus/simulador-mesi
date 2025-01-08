import sys

'''
Deve-se implementar um simulador simplificado para o protocolo de coerência de cache MESI em
processadores com memória compartilhada centralizada.

• Não é necessária a implementação de nenhum outro modulo do simulador além do
sistema de memória (Memória principal e cache).
• O sistema de memória deve ter no mínimo três níveis
◦ Memória principal (compartilhada);
◦ Memória cache compartilhada;
◦ Cache privada de cada processador (dividida em dados e instruções);
• A memória principal deve possuir um total de 32 bits para endereços
• O tipo de mapeamento de cache fica a critério da equipe podendo ser um dos dois:
◦ Mapeamento associativo;
◦ Mapeamento associativo por conjunto;
• Como as operações em memória não serão de fato realizadas, não é necessário
implementar uma politica de escrita para a atualização de MP ou cache
compartilhada.
• O deve ser possível configurar as seguintes características da cache:
◦ Tamanho da linha (tamanho do bloco de MP);
▪ Deve ser o mesmo para as caches privadas e compartilhada
◦ Número de linhas da cache;
▪ O número de linhas das caches privadas deve ser menor que o número de
linhas da cache compartilhada.
▪ Devem ser respeitadas as características do tipo de mapeamento escolhido
• Detalhes do número de conjunto ou outras caracteristicas.
◦ Algoritmo de substituição de linha de cache
▪ Deverão ser implementados no mínimo dois algoritmos de substituição de
linha.
◦ Caso seja de vontade da equipe, é permitido que o mapeamento também seja uma
configuração da cache;
• Além disso, deve ser informado a quantidade de processadores que o sistema possui
(usado para determinar a quantidade de caches privadas)
Configurações e entradas

As configurações devem ser fornecidas para o simulador de uma das seguintes maneiras:
• Argumentos na linha de comando;
• Arquivo de entrada com configurações;
Além das configurações do sistema de memória, também deverá ser fornecido como entrada um
arquivo contendo uma sequência de acessos a memória, onde cada linha deste arquivo representa
um acesso à memória feito por um processador.
Cada linha dos arquivos de entrada possuem o seguinte formato:
<id do processador> <tipo de operação> <endereço acessado>
Onde:
<id do processador>: é um valor inteiro entre 0 e o número de processadores do sistema
(configurado na execução)
<tipo de operação>: determina se aquele acesso a memória é:
• 0: Leitura de instruções;
• 2: Leitura de dados;
• 3: Escrita de dados;
<endereço acessado>: um valor hexadecimal que corresponde ao endereço da MP o qual foi
realizada a operação pelo processador indicado na linha

Para facilitar a implementação, assuma que somente uma requisição para qualquer endereço de
memória será feita por instante de tempo, e a ordem das requisições é a mesma apresentada no
arquivo.
Um conjunto de arquivos de teste está disponível para download no Classroom da disciplina no
mesmo tópico desta especificação.

Saída

Como saída, espera-se que a cada solicitação de memória seja mostrado:
• A operação realizada, o endereço no qual ela foi feita e o processador que a realizou
◦ Em outras palavras, a linha do arquivo de entrada;
• A mensagem enviada no barramento devido a realização daquela operação;
• O estado da cache privada de cada processador;
◦ Quais blocos estão em cache cada linha da cache;
◦ Qual o estado de cada bloco;
• Os dados que estão na cache compartilhada
A saída pode ser mostrada em tela (com uma interface gráfica ou um terminal) ou um arquivo de
log deve ser gerado.
• Caso a equipe prefira, ambos podem ser feitos simultaneamente.

'''
### AREA DE CONFIGURAÇÃO DO SIMULADOR ###
# Será um arquivo de configuração
n_linhas = 8
tamanho_do_bloco = 32

class MemoriaPrincipal:
    def __init__(self):
        # Usando um dicionário para simular a memória principal
        # As chaves são endereços em hexadecimal (representados como strings)
        self.dados = {}

    def read(self, endereco: str) -> int:
        """
        Lê um valor na memória no endereço fornecido em hexadecimal.
        """
        endereco_em_int = int(endereco, 16)  # Converte o endereço hexadecimal para inteiro
        if not (0 <= endereco_em_int < 2**32):
            raise ValueError("Endereço fora do espaço de endereçamento de 32 bits.")
        return self.data.get(endereco_em_int, 0)  # Retorna 0 se o endereço não tiver dado

    def write(self, endereco: str):
        """
        Escreve um valor na memória no endereço fornecido em hexadecimal.
        """
        endereco_em_int = int(endereco, 16)  # Converte o endereço hexadecimal para inteiro
        if not (0 <= endereco_em_int < 2**32):
            raise ValueError("Endereço fora do espaço de endereçamento de 32 bits.")
        self.data[endereco] = endereco  # Armazena o valor com a chave hexadecimal

class LinhaCache:
    def __init__(self):
        self.tag = None
        self.n_acessos = 0
        self.estado = 'I'
        self.dados = None # Poderá ser removido no futuro (?)


class Cache:
    def __init__(self):
        self.linhas = []
        for i in range(n_linhas):
            self.linhas.append(LinhaCache())
        self.tamanho_do_bloco = tamanho_do_bloco


def leitura_arquivo_configuracao():
    '''
    Realiza a leitura do arquivo de configuração.
    É necessário que o arquivo de configuração esteja no mesmo diretório do arquivo principal.
    O nome do arquivo deve ser "settings.ini"
    '''
    arq_configuracao = open('settings.ini', 'r')
    linhas = arq_configuracao.readlines()

    global NUMERO_PROCESSADORES
    NUMERO_PROCESSADORES = int(linhas[0].split('=')[1])

    global TAMANHO_LINHA
    TAMANHO_LINHA = int(linhas[1].split('=')[1])

    global NUMERO_LINHAS_CACHE
    NUMERO_LINHAS_CACHE = int(linhas[2].split('=')[1])


def le_instrucoes(arquivo) -> list:
    with open(arquivo, 'r') as f:
        instrucoes = f.readlines()
    return instrucoes

def carrega_memoria_principal(mem_principal: MemoriaPrincipal) -> int:
    nome_arq = le_instrucoes(input('Digite o nome do arquivo de instruções: '))
    arq_entrada = open(nome_arq,'r')
    instrucoes = arq_entrada.readlines()
    for i in instrucoes:
        instrucao = i.strip().split(' ')
        mem_principal.write(instrucao[0],instrucao[1]) # Nao sei como fazer isso ainda
        # Processa a instrução

