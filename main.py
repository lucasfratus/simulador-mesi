import sys
import config

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


class LinhaCache:
    def __init__(self):
        self.bloco = []
        self.contador = -1
        self.estado = 'I'

    def __str__(self):
        return f'Est: {self.estado} - Bloco: {self.bloco}'
    
    def invalidate(self):
        self.bloco = []
        self.estado = 'I'

    def write(self, bloco):
        self.bloco = bloco
        self.estado = 'M'


class Cache:
    def __init__(self, n_linhas, n_linhas_por_conjunto):
        self.conjuntos = {}
        for i in range(n_linhas//n_linhas_por_conjunto):
            self.conjuntos[i] = [LinhaCache() for j in range(n_linhas_por_conjunto)]

    def __str__(self):
        retorno = ''
        for conjunto in self.conjuntos:
            retorno += f'Conjunto {conjunto}:\n'
            for linha in self.conjuntos[conjunto]:
                retorno += f'{linha}\n'
            retorno += '\n'
        return retorno


def le_instrucoes(arquivo) -> list:
    with open(arquivo, 'r') as f:
        instrucoes = f.readlines()
    return instrucoes


def separa_instrucao(instrucao: str) -> tuple:
    instrucao = instrucao.split()
    return (int(instrucao[0]), int(instrucao[1]), str(instrucao[2]))


def leitura_arquivo_configuracao():
    '''
    Realiza a leitura do arquivo de configuração.
    É necessário que o arquivo de configuração esteja no mesmo diretório do arquivo principal.
    O nome do arquivo deve ser "settings.ini"
    '''
    #arq_configuracao = open('settings.ini', 'r')
    #linhas = arq_configuracao.readlines()

    global NUMERO_PROCESSADORES
    #NUMERO_PROCESSADORES = int(linhas[0].split('=')[1])
    NUMERO_PROCESSADORES = config.CONFIGURACOES['n_processadores']

    global TAMANHO_LINHA    #  == tamanho do bloco
    #TAMANHO_LINHA = int(linhas[1].split('=')[1])
    TAMANHO_LINHA = config.CONFIGURACOES['tamanho_linha']

    global NUMERO_LINHAS_CACHE_COMPARTILHADA
    #NUMERO_LINHAS_CACHE_COMPARTILHADA = int(linhas[2].split('=')[1])
    NUMERO_LINHAS_CACHE_COMPARTILHADA = config.CONFIGURACOES['n_linhas_cache_compartilhada']

    global NUMERO_LINHAS_CACHE_PRIVADA
    #NUMERO_LINHAS_CACHE_PRIVADA = int(linhas[3].split('=')[1])
    NUMERO_LINHAS_CACHE_PRIVADA = config.CONFIGURACOES['n_linhas_cache_privada']

    if NUMERO_LINHAS_CACHE_PRIVADA >= NUMERO_LINHAS_CACHE_COMPARTILHADA:
        raise ValueError('O número de linhas da cache privada deve ser menor que o número de linhas da cache compartilhada.')

    global NUMERO_LINHAS_CONJUNTO
    #NUMERO_LINHAS_CONJUNTO = int(linhas[4].split('=')[1])
    NUMERO_LINHAS_CONJUNTO = config.CONFIGURACOES['n_linhas_conjunto']

    if NUMERO_LINHAS_CACHE_PRIVADA % NUMERO_LINHAS_CONJUNTO != 0:
        raise ValueError('O número de linhas da cache privada deve ser múltiplo do número de linhas por conjunto.')
    
    if NUMERO_LINHAS_CACHE_COMPARTILHADA % NUMERO_LINHAS_CONJUNTO != 0:
        raise ValueError('O número de linhas da cache compartilhada deve ser múltiplo do número de linhas por conjunto.')
    
    global POLITICA_SUBSTITUICAO
    #POLITICA_SUBSTITUICAO = linhas[5].split('=')[1].strip()
    POLITICA_SUBSTITUICAO = config.CONFIGURACOES['politica_substituicao']

    if POLITICA_SUBSTITUICAO not in ['LFU', 'FIFO']:
        raise ValueError('A política de substituição deve ser LFU ou FIFO.')


def main():
    leitura_arquivo_configuracao()
    print(f'Numero de processadores: {NUMERO_PROCESSADORES}')
    print(f'Tamanho da linha: {TAMANHO_LINHA}')
    print(f'Numero de linhas da cache compartilhada: {NUMERO_LINHAS_CACHE_COMPARTILHADA}')
    print(f'Numero de linhas da cache privada: {NUMERO_LINHAS_CACHE_PRIVADA}')
    print(f'Numero de linhas por conjunto: {NUMERO_LINHAS_CONJUNTO}')
    print(f'Politica de substituição: {POLITICA_SUBSTITUICAO}')

    cache_compartilhada_dados = Cache(NUMERO_LINHAS_CACHE_COMPARTILHADA, NUMERO_LINHAS_CONJUNTO)
    cache_compartilhada_instrucoes = Cache(NUMERO_LINHAS_CACHE_COMPARTILHADA, NUMERO_LINHAS_CONJUNTO) 

    cache_privada_dados = []
    cache_privada_instrucoes = []
    for i in range(NUMERO_PROCESSADORES):
        cache_privada_dados.append(Cache(NUMERO_LINHAS_CACHE_PRIVADA, NUMERO_LINHAS_CONJUNTO))
        cache_privada_instrucoes.append(Cache(NUMERO_LINHAS_CACHE_PRIVADA, NUMERO_LINHAS_CONJUNTO))

    instr = le_instrucoes('instrucoes.txt')

    if POLITICA_SUBSTITUICAO == 'LFU':
        LFU(cache_privada_dados, cache_privada_instrucoes, cache_compartilhada_dados, cache_compartilhada_instrucoes, instr)
    else:
        FIFO(cache_privada_dados, cache_privada_instrucoes, cache_compartilhada_dados, cache_compartilhada_instrucoes, instr)
    

def FIFO(cache_privada_dados, cache_privada_instrucoes, cache_compartilhada_dados, cache_compartilhada_instrucoes, instrucoes):
    for instrucao in instrucoes:
        processador, operacao, endereco = separa_instrucao(instrucao)
        print(f'Processador: {processador} - Operacao: {operacao} - Endereco: {endereco}')

        match operacao:
            case 0:
                # Leitura de instrucoes

                #busca na cache privada
                hit = False
                conjunto_privada = int(endereco, 16) % (NUMERO_LINHAS_CACHE_PRIVADA // NUMERO_LINHAS_CONJUNTO)
                for linha in cache_privada_instrucoes[processador].conjuntos[conjunto_privada]:
                    if endereco in linha.bloco and linha.estado != 'I':
                        print('Hit na cache privada de instrucoes')
                        hit = True
                        break
                if not hit:
                    print('Miss na cache privada de instrucoes')
                    #busca na cache compartilhada
                    conjunto_compartilhada = int(endereco, 16) % (NUMERO_LINHAS_CACHE_COMPARTILHADA // NUMERO_LINHAS_CONJUNTO)
                    for linha in cache_compartilhada_instrucoes.conjuntos[conjunto_compartilhada]:
                        if endereco in linha.bloco and linha.estado != 'I':
                            print('Hit na cache compartilhada de instrucoes')
                            hit = True
                            for i in range(NUMERO_PROCESSADORES):
                                for linha_privada in cache_privada_instrucoes[i].conjuntos[conjunto_privada]:
                                    if linha_privada.estado == 'M' or linha_privada.estado == 'E':
                                        linha_privada.estado = 'S'

                            # Atualiza a cache privada
                            inserido = False
                            for linha_p in cache_privada_instrucoes[processador].conjuntos[conjunto_privada]:
                                linha_p.contador += 1
                                if linha_p.estado == 'I':
                                    linha_p.bloco = linha.bloco
                                    linha_p.estado = 'S'
                                    linha_p.contador = 0
                                    inserido = True
                                    

                            if not inserido:
                                maior = -1
                                linha_substituida = None
                                for linha_p in cache_privada_instrucoes[processador].conjuntos[conjunto_privada]:
                                    if linha_p.contador > maior:
                                        maior = linha_p.contador
                                        linha_substituida = linha_p
                                linha_substituida.bloco = linha.bloco
                                linha_substituida.estado = 'S'
                                linha_substituida.contador = 0
                                    
                            break
                    if not hit:
                        print('Miss na cache compartilhada de instrucoes')
                        #busca nos outros processadores
                        #busca na memoria principal
                        ...


            case 2:
                # Leitura de dados

                # TODO: Implementar a leitura de dados
                hit = False

                # Busca na cache privada
                conjunto_privada = int(endereco, 16) % (NUMERO_LINHAS_CACHE_PRIVADA // NUMERO_LINHAS_CONJUNTO)

                for linha in cache_privada_dados[processador].conjuntos[conjunto_privada]:
                    if endereco in linha.bloco and linha.estado != 'I':
                        print('Hit na cache privada de dados')
                        hit = True
                        break

                if not hit:
                    print('Miss na cache privada de dados')

                    # Busca na cache compartilhada
                    conjunto_compartilhada = int(endereco, 16) % (NUMERO_LINHAS_CACHE_COMPARTILHADA // NUMERO_LINHAS_CONJUNTO)

                    # Verifica se o bloco está na cache compartilhada
                    for linha in cache_compartilhada_dados.conjuntos[conjunto_compartilhada]:
                        if endereco in linha.bloco and linha.estado != 'I':
                            print('Hit na cache compartilhada de dados')
                            hit = True
                            for i in range(NUMERO_PROCESSADORES):
                                for linha_privada in cache_privada_dados[i].conjuntos[conjunto_privada]:
                                    if linha_privada.estado == 'M' or linha_privada.estado == 'E': # TODO: VERIFICAR SE ESTÁ CERTO
                                        linha_privada.estado = 'S'

                            # Atualiza a cache privada
                            inserido = False
                            for linha_p in cache_privada_dados[processador].conjuntos[conjunto_privada]:
                                linha_p.contador += 1
                                if linha_p.estado == 'I':
                                    linha_p.bloco = linha.bloco
                                    linha_p.estado = 'S'
                                    linha_p.contador = 0
                                    inserido = True
                                    

                            if not inserido:
                                maior = -1
                                linha_substituida = None
                                for linha_p in cache_privada_dados[processador].conjuntos[conjunto_privada]:
                                    if linha_p.contador > maior:
                                        maior = linha_p.contador
                                        linha_substituida = linha_p
                                linha_substituida.bloco = linha.bloco
                                linha_substituida.estado = 'S'
                                linha_substituida.contador = 0    
                            break
            case 3:
                # Escrita de dados
                pass
        


def LFU(cache_privada_dados, cache_privada_instrucoes, cache_compartilhada_dados, cache_compartilhada_instrucoes, instrucoes):
    pass


main()
