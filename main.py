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





def imprimir_caches(cache_privada_dados, cache_privada_instrucoes, cache_compartilhada_dados, cache_compartilhada_instrucoes, arq_log):
    arq_log.write('Cache privada de dados:\n\n')
    print('Cache privada de dados:')
    for i in range(len(cache_privada_dados)):
        arq_log.write(f'Processador {i}:\n\n')
        print(f'Processador {i}:')
        arq_log.write(str(cache_privada_dados[i]))
        print(cache_privada_dados[i])
    print('Cache privada de instrucoes:')
    arq_log.write('Cache privada de instrucoes:\n\n')
    for i in range(len(cache_privada_instrucoes)):
        arq_log.write(f'Processador {i}:\n\n')
        print(f'Processador {i}:')
        arq_log.write(str(cache_privada_instrucoes[i]))
        print(cache_privada_instrucoes[i])
    print('Cache compartilhada de dados:')
    arq_log.write('Cache compartilhada de dados:\n\n')
    print(cache_compartilhada_dados)
    arq_log.write(str(cache_compartilhada_dados))
    print('Cache compartilhada de instrucoes:')
    arq_log.write('Cache compartilhada de instrucoes:\n\n')
    print(cache_compartilhada_instrucoes)
    arq_log.write(str(cache_compartilhada_instrucoes))
    arq_log.write('\n\n')


def separa_instrucao(instrucao: str) -> tuple:
    instrucao = instrucao.split()
    return (int(instrucao[0]), int(instrucao[1]), str(instrucao[2]))


def leitura_arquivo_configuracao():
    '''
    Realiza a leitura do arquivo de configuração.
    É necessário que o arquivo de configuração esteja no mesmo diretório do arquivo principal.
    '''
    global NUMERO_PROCESSADORES
    NUMERO_PROCESSADORES = config.CONFIGURACOES['n_processadores']

    global TAMANHO_LINHA    #  == tamanho do bloco
    TAMANHO_LINHA = config.CONFIGURACOES['tamanho_linha']

    global NUMERO_LINHAS_CACHE_COMPARTILHADA
    NUMERO_LINHAS_CACHE_COMPARTILHADA = config.CONFIGURACOES['n_linhas_cache_compartilhada']

    global NUMERO_LINHAS_CACHE_PRIVADA
    NUMERO_LINHAS_CACHE_PRIVADA = config.CONFIGURACOES['n_linhas_cache_privada']

    if NUMERO_LINHAS_CACHE_PRIVADA * NUMERO_PROCESSADORES >= NUMERO_LINHAS_CACHE_COMPARTILHADA:
        raise ValueError('O número de linhas da cache privada deve ser menor que o número somado de linhas de todas as caches compartilhadas.')

    global NUMERO_LINHAS_CONJUNTO
    NUMERO_LINHAS_CONJUNTO = config.CONFIGURACOES['n_linhas_conjunto']

    if NUMERO_LINHAS_CACHE_PRIVADA % NUMERO_LINHAS_CONJUNTO != 0:
        raise ValueError('O número de linhas da cache privada deve ser múltiplo do número de linhas por conjunto.')
    
    if NUMERO_LINHAS_CACHE_COMPARTILHADA % NUMERO_LINHAS_CONJUNTO != 0:
        raise ValueError('O número de linhas da cache compartilhada deve ser múltiplo do número de linhas por conjunto.')
    
    if TAMANHO_LINHA == 0:
        raise ValueError('O tamanho da linha deve ser maior que 0.')

    global POLITICA_SUBSTITUICAO
    POLITICA_SUBSTITUICAO = config.CONFIGURACOES['politica_substituicao']

    if POLITICA_SUBSTITUICAO not in ['LFU', 'FIFO']:
        raise ValueError('A política de substituição deve ser LFU ou FIFO.')


def main():
    arq_log = open('log.txt', 'w')
    leitura_arquivo_configuracao()
    print(f'Numero de processadores: {NUMERO_PROCESSADORES}')
    arq_log.write(f'Numero de processadores: {NUMERO_PROCESSADORES}\n')
    print(f'Tamanho da linha: {TAMANHO_LINHA}')
    arq_log.write(f'Tamanho da linha: {TAMANHO_LINHA}\n')
    print(f'Numero de linhas da cache compartilhada: {NUMERO_LINHAS_CACHE_COMPARTILHADA}')
    arq_log.write(f'Numero de linhas da cache compartilhada: {NUMERO_LINHAS_CACHE_COMPARTILHADA}\n')
    print(f'Numero de linhas da cache privada: {NUMERO_LINHAS_CACHE_PRIVADA}')
    arq_log.write(f'Numero de linhas da cache privada: {NUMERO_LINHAS_CACHE_PRIVADA}\n')
    print(f'Numero de linhas por conjunto: {NUMERO_LINHAS_CONJUNTO}')
    arq_log.write(f'Numero de linhas por conjunto: {NUMERO_LINHAS_CONJUNTO}\n')
    print(f'Politica de substituição: {POLITICA_SUBSTITUICAO}')

    cache_compartilhada_dados = Cache(NUMERO_LINHAS_CACHE_COMPARTILHADA, NUMERO_LINHAS_CONJUNTO)
    cache_compartilhada_instrucoes = Cache(NUMERO_LINHAS_CACHE_COMPARTILHADA, NUMERO_LINHAS_CONJUNTO) 

    cache_privada_dados = []
    cache_privada_instrucoes = []
    for i in range(NUMERO_PROCESSADORES):
        cache_privada_dados.append(Cache(NUMERO_LINHAS_CACHE_PRIVADA, NUMERO_LINHAS_CONJUNTO))
        cache_privada_instrucoes.append(Cache(NUMERO_LINHAS_CACHE_PRIVADA, NUMERO_LINHAS_CONJUNTO))


    arq_instrucoes = open('instrucoes.txt', 'r')

    if POLITICA_SUBSTITUICAO == 'LFU':
        LFU(cache_privada_dados, cache_privada_instrucoes, cache_compartilhada_dados, cache_compartilhada_instrucoes, arq_instrucoes, arq_log)
    else:
        FIFO(cache_privada_dados, cache_privada_instrucoes, cache_compartilhada_dados, cache_compartilhada_instrucoes, arq_instrucoes, arq_log)

    arq_instrucoes.close()
    

def FIFO(cache_privada_dados, cache_privada_instrucoes, cache_compartilhada_dados, cache_compartilhada_instrucoes, arq_instrucoes, arq_log):
    instrucao_atual = arq_instrucoes.readline()
    print(instrucao_atual)
    arq_log.write(instrucao_atual)
    while instrucao_atual:
        processador, operacao, endereco = separa_instrucao(instrucao_atual)
        if processador >= NUMERO_PROCESSADORES:
            raise ValueError('O id do processador não pode ser maior que o número de processadores.')
        elif operacao not in [0, 2, 3]:
            raise ValueError('O tipo de operação deve ser 0, 2 ou 3.')
        elif len(endereco) != 8:
            raise ValueError('O endereço deve ter 8 caracteres (4 bytes).')
        
        print(f'Processador: {processador} - Operacao: {operacao} - Endereco: {endereco}')
        arq_log.write(f'Processador: {processador} - Operacao: {operacao} - Endereco: {endereco}\n')

        match operacao:
            case 0:
                # Leitura de instrucoes
                hit = False
                conjunto_privada = int(endereco, 16) % (NUMERO_LINHAS_CACHE_PRIVADA // NUMERO_LINHAS_CONJUNTO)
                # Verifica se há um hit na cache privada de instruções
                for linha in cache_privada_instrucoes[processador].conjuntos[conjunto_privada]: # tentar encontrar o bloco em seu respectivo conjunto
                    if endereco in linha.bloco and linha.estado != 'I':
                        print('Read Hit na cache privada de instrucoes')
                        arq_log.write('Read Hit na cache privada de instrucoes\n\n')
                        hit = True
                        break
                if not hit:
                    print('Miss na cache privada de instrucoes')
                    arq_log.write('Miss na cache privada de instrucoes\n\n')
                    print('Buscando na cache compartilhada de instrucoes')
                    arq_log.write('Buscando na cache compartilhada de instrucoes\n\n')
                    conjunto_compartilhada = int(endereco, 16) % (NUMERO_LINHAS_CACHE_COMPARTILHADA // NUMERO_LINHAS_CONJUNTO)
                    # Verifica se há um hit na cache compartilhada de instruções
                    for linha in cache_compartilhada_instrucoes.conjuntos[conjunto_compartilhada]:
                        if endereco in linha.bloco and linha.estado != 'I':
                            print('Hit na cache compartilhada de instrucoes')
                            hit = True
                            linha.estado = 'S'
                            # Atualiza o estado das linhas na cache privada de todos os processadores
                            for i in range(NUMERO_PROCESSADORES):
                                for linha_privada in cache_privada_instrucoes[i].conjuntos[conjunto_privada]:
                                    if linha_privada.estado in ['M', 'E']:
                                        linha_privada.estado = 'S'
                            # Insere o bloco na cache privada do processador atual
                            inserido = False
                            for linha_p in cache_privada_instrucoes[processador].conjuntos[conjunto_privada]:
                                linha_p.contador += 1
                                if linha_p.estado == 'I' and inserido == False:
                                    linha_p.bloco = linha.bloco
                                    linha_p.estado = 'S'
                                    linha_p.contador = 0
                                    inserido = True
                            if not inserido:
                                maior = max(cache_privada_instrucoes[processador].conjuntos[conjunto_privada], key=lambda l: l.contador)
                                maior.bloco = linha.bloco
                                maior.estado = 'S'
                                maior.contador = 0
                            break
                    if not hit:
                        print('Miss na cache compartilhada de instrucoes')
                        arq_log.write('Miss na cache compartilhada de instrucoes\n\n')
                        print('Buscando na memoria principal')
                        arq_log.write('Buscando na memoria principal\n\n')
                        bloco_memoria_principal = [hex(int(endereco, 16) - (int(endereco, 16) % TAMANHO_LINHA) + i) for i in range(TAMANHO_LINHA)]
                        # Insere o bloco na cache compartilhada
                        inserido = False
                        for linha_c in cache_compartilhada_instrucoes.conjuntos[conjunto_compartilhada]:
                            linha_c.contador += 1
                            if linha_c.estado == 'I' and inserido == False:
                                linha_c.bloco = bloco_memoria_principal
                                linha_c.estado = 'E'
                                linha_c.contador = 0
                                inserido = True
                        if not inserido:
                            maior = max(cache_compartilhada_instrucoes.conjuntos[conjunto_compartilhada], key=lambda l: l.contador)
                            maior.bloco = bloco_memoria_principal
                            maior.estado = 'E'
                            maior.contador = 0
                        # Insere o bloco na cache privada do processador atual
                        inserido = False
                        for linha_p in cache_privada_instrucoes[processador].conjuntos[conjunto_privada]:
                            linha_p.contador += 1
                            if linha_p.estado == 'I' and inserido == False:
                                linha_p.bloco = bloco_memoria_principal
                                linha_p.estado = 'E'
                                linha_p.contador = 0
                                inserido = True
                        if not inserido:
                            maior = max(cache_privada_instrucoes[processador].conjuntos[conjunto_privada], key=lambda l: l.contador)
                            maior.bloco = bloco_memoria_principal
                            maior.estado = 'E'
                            maior.contador = 0

            case 2:
                # Leitura de dados
                hit = False
                conjunto_privada = int(endereco, 16) % (NUMERO_LINHAS_CACHE_PRIVADA // NUMERO_LINHAS_CONJUNTO)
                # Verifica se há um hit na cache privada de dados
                for linha in cache_privada_dados[processador].conjuntos[conjunto_privada]:
                    if endereco in linha.bloco and linha.estado != 'I':
                        print('Read Hit na cache privada de dados')
                        arq_log.write('Read Hit na cache privada de dados\n\n')
                        hit = True
                        break
                if not hit:
                    print('Read Miss na cache privada de dados')
                    arq_log.write('Read Miss na cache privada de dados\n\n')
                    print('Buscando na cache compartilhada de dados\n\n')
                    arq_log.write('Buscando na cache compartilhada de dados\n\n')
                    conjunto_compartilhada = int(endereco, 16) % (NUMERO_LINHAS_CACHE_COMPARTILHADA // NUMERO_LINHAS_CONJUNTO)
                    # Verifica se há um hit na cache compartilhada de dados
                    for linha in cache_compartilhada_dados.conjuntos[conjunto_compartilhada]:
                        if endereco in linha.bloco and linha.estado != 'I':
                            print('Read Hit na cache compartilhada de dados')
                            arq_log.write('Read Hit na cache compartilhada de dados\n\n')
                            hit = True
                            linha.estado = 'S'
                            # Atualiza o estado das linhas na cache privada de todos os processadores
                            for i in range(NUMERO_PROCESSADORES):
                                for linha_privada in cache_privada_dados[i].conjuntos[conjunto_privada]:
                                    if linha_privada.estado in ['M', 'E']:
                                        linha_privada.estado = 'S'
                            # Insere o bloco na cache privada do processador atual
                            inserido = False
                            for linha_p in cache_privada_dados[processador].conjuntos[conjunto_privada]:
                                linha_p.contador += 1
                                if linha_p.estado == 'I' and inserido == False:
                                    linha_p.bloco = linha.bloco
                                    linha_p.estado = 'S'
                                    linha_p.contador = 0
                                    inserido = True
                            if not inserido:
                                maior = max(cache_privada_dados[processador].conjuntos[conjunto_privada], key=lambda l: l.contador)
                                maior.bloco = linha.bloco
                                maior.estado = 'S'
                                maior.contador = 0
                            break
                    if not hit:
                        print('Read Miss na cache compartilhada de dados')
                        arq_log.write('Read Miss na cache compartilhada de dados\n\n')
                        print('Buscando na memoria principal')
                        arq_log.write('Buscando na memoria principal\n\n')
                        bloco_memoria_principal = [hex(int(endereco, 16) - (int(endereco, 16) % TAMANHO_LINHA) + i) for i in range(TAMANHO_LINHA)]
                        # Insere o bloco na cache compartilhada
                        inserido = False
                        for linha_c in cache_compartilhada_dados.conjuntos[conjunto_compartilhada]:
                            linha_c.contador += 1
                            if linha_c.estado == 'I' and inserido == False:
                                linha_c.bloco = bloco_memoria_principal
                                linha_c.estado = 'E'
                                linha_c.contador = 0
                                inserido = True
                        if not inserido:
                            maior = max(cache_compartilhada_dados.conjuntos[conjunto_compartilhada], key=lambda l: l.contador)
                            maior.bloco = bloco_memoria_principal
                            maior.estado = 'E'
                            maior.contador = 0
                        # Insere o bloco na cache privada do processador atual
                        inserido = False
                        for linha_p in cache_privada_dados[processador].conjuntos[conjunto_privada]:
                            linha_p.contador += 1
                            if linha_p.estado == 'I' and inserido == False:
                                linha_p.bloco = bloco_memoria_principal
                                linha_p.estado = 'E'
                                linha_p.contador = 0
                                inserido = True
                        if not inserido:
                            maior = max(cache_privada_dados[processador].conjuntos[conjunto_privada], key=lambda l: l.contador)
                            maior.bloco = bloco_memoria_principal
                            maior.estado = 'E'
                            maior.contador = 0

            case 3:
                # Escrita de dados
                hit = False
                conjunto_privada = int(endereco, 16) % (NUMERO_LINHAS_CACHE_PRIVADA // NUMERO_LINHAS_CONJUNTO)
                # Verifica se há um hit na cache privada de dados
                for linha in cache_privada_dados[processador].conjuntos[conjunto_privada]:
                    if endereco in linha.bloco and linha.estado != 'I':
                        print('Write Hit na cache privada de dados')
                        arq_log.write('Write Hit na cache privada de dados\n\n')
                        hit = True
                        linha.estado = 'M'
                        # Invalida o estado das linhas na cache privada de todos os processadores
                        for i in range(NUMERO_PROCESSADORES):
                            for linha_privada in cache_privada_dados[i].conjuntos[conjunto_privada]:
                                if endereco in linha_privada.bloco:
                                    linha_privada.estado = 'I'
                        # Invalida o estado das linhas na cache compartilhada
                        for linha_c in cache_compartilhada_dados.conjuntos[conjunto_privada]:
                            if endereco in linha_c.bloco:
                                linha_c.estado = 'I'
                        break
                if not hit:
                    print('Write Miss na cache privada de dados')
                    arq_log.write('Write Miss na cache privada de dados\n\n')
                    print('Buscando na cache compartilhada de dados')
                    arq_log.write('Buscando na cache compartilhada de dados\n\n')
                    conjunto_compartilhada = int(endereco, 16) % (NUMERO_LINHAS_CACHE_COMPARTILHADA // NUMERO_LINHAS_CONJUNTO)
                    # Verifica se há um hit na cache compartilhada de dados
                    for linha in cache_compartilhada_dados.conjuntos[conjunto_compartilhada]:
                        if endereco in linha.bloco and linha.estado != 'I':
                            print('Hit na cache compartilhada de dados')
                            arq_log.write('Hit na cache compartilhada de dados\n\n')
                            hit = True
                            linha.estado = 'M'
                            # Invalida o estado das linhas na cache privada de todos os processadores
                            for i in range(NUMERO_PROCESSADORES):
                                for linha_privada in cache_privada_dados[i].conjuntos[conjunto_privada]:
                                    if endereco in linha_privada.bloco:
                                        linha_privada.estado = 'I'
                            # Invalida o estado das linhas na cache compartilhada
                            for linha_c in cache_compartilhada_dados.conjuntos[conjunto_privada]:
                                if endereco in linha_c.bloco:
                                    linha_c.estado = 'I'
                            # Insere o bloco na cache privada do processador atual
                            inserido = False
                            for linha_p in cache_privada_dados[processador].conjuntos[conjunto_privada]:
                                if linha_p.estado == 'I' and inserido == False:
                                    linha_p.bloco = linha.bloco
                                    linha_p.estado = 'M'
                                    inserido = True
                            if not inserido:
                                maior = max(cache_privada_dados[processador].conjuntos[conjunto_privada], key=lambda l: l.contador)
                                maior.bloco = linha.bloco
                                maior.estado = 'M'
                            break
                    if not hit:
                        print('Write Miss na cache compartilhada de dados')
                        arq_log.write('Write Miss na cache compartilhada de dados\n\n')
                        print('Buscando na memoria principal')
                        arq_log.write('Buscando na memoria principal\n\n')
                        bloco_memoria_principal = [hex(int(endereco, 16) - (int(endereco, 16) % TAMANHO_LINHA) + i) for i in range(TAMANHO_LINHA)]
                        # Insere o bloco na cache compartilhada
                        inserido = False
                        for linha_c in cache_compartilhada_dados.conjuntos[conjunto_compartilhada]:
                            if linha_c.estado == 'I':
                                linha_c.bloco = bloco_memoria_principal
                                linha_c.estado = 'M'
                                inserido = True
                                break
                        if not inserido:
                            maior = max(cache_compartilhada_dados.conjuntos[conjunto_compartilhada], key=lambda l: l.contador)
                            maior.bloco = bloco_memoria_principal
                            maior.estado = 'M'
                        # Insere o bloco na cache privada do processador atual
                        inserido = False
                        for linha_p in cache_privada_dados[processador].conjuntos[conjunto_privada]:
                            linha_p.contador += 1
                            if linha_p.estado == 'I' and inserido == False:
                                linha_p.bloco = bloco_memoria_principal
                                linha_p.estado = 'E'
                                linha_p.contador = 0
                                inserido = True
                        if not inserido:
                            maior = max(cache_privada_dados[processador].conjuntos[conjunto_privada], key=lambda l: l.contador)
                            maior.bloco = bloco_memoria_principal
                            maior.estado = 'E'
                            maior.contador = 0
        imprimir_caches(cache_privada_dados, cache_privada_instrucoes, cache_compartilhada_dados, cache_compartilhada_instrucoes, arq_log)
        instrucao_atual = arq_instrucoes.readline()


def LFU(cache_privada_dados, cache_privada_instrucoes, cache_compartilhada_dados, cache_compartilhada_instrucoes, instrucoes, arq_log):
    instrucao_atual = instrucoes.readline()
    while instrucao_atual:
        processador, operacao, endereco = separa_instrucao(instrucao_atual)
        if processador >= NUMERO_PROCESSADORES:
            raise ValueError('O id do processador não pode ser maior que o número de processadores.')
        elif operacao not in [0, 2, 3]:
            raise ValueError('O tipo de operação deve ser 0, 2 ou 3.')
        elif len(endereco) != 8:
            raise ValueError('O endereço deve ter 8 caracteres (4 bytes).')
        
        print(f'Processador: {processador} - Operacao: {operacao} - Endereco: {endereco}')
        arq_log.write(f'Processador: {processador} - Operacao: {operacao} - Endereco: {endereco}\n')
        match operacao:
            case 0:
                # Leitura de instrucoes
                hit = False
                conjunto_privada = int(endereco, 16) % (NUMERO_LINHAS_CACHE_PRIVADA // NUMERO_LINHAS_CONJUNTO)
                # Verifica se há um hit na cache privada de instruções
                for linha in cache_privada_instrucoes[processador].conjuntos[conjunto_privada]: # tentar encontrar o bloco em seu respectivo conjunto
                    if endereco in linha.bloco and linha.estado != 'I':
                        print('Hit na cache privada de instrucoes')
                        arq_log.write('Hit na cache privada de instrucoes\n\n')
                        hit = True
                        linha.contador += 1
                        break
                if not hit:
                    print('Miss na cache privada de instrucoes')
                    arq_log.write('Miss na cache privada de instrucoes\n\n')
                    conjunto_compartilhada = int(endereco, 16) % (NUMERO_LINHAS_CACHE_COMPARTILHADA // NUMERO_LINHAS_CONJUNTO)
                    # Verifica se há um hit na cache compartilhada de instruções
                    for linha in cache_compartilhada_instrucoes.conjuntos[conjunto_compartilhada]:
                        if endereco in linha.bloco and linha.estado != 'I':
                            print('Hit na cache compartilhada de instrucoes')
                            arq_log.write('Hit na cache compartilhada de instrucoes\n\n')
                            hit = True
                            linha.contador += 1
                            linha.estado = 'S' 
                            # Atualiza o estado das linhas na cache privada de todos os processadores
                            for i in range(NUMERO_PROCESSADORES):
                                for linha_privada in cache_privada_instrucoes[i].conjuntos[conjunto_privada]:
                                    if linha_privada.estado in ['M', 'E']:
                                        linha_privada.estado = 'S'
                            # Insere o bloco na cache privada do processador atual
                            inserido = False
                            for linha_p in cache_privada_instrucoes[processador].conjuntos[conjunto_privada]:
                                if linha_p.estado == 'I':
                                    linha_p.bloco = linha.bloco
                                    linha_p.estado = 'S'
                                    linha_p.contador = 1
                                    inserido = True
                                    break
                            if not inserido:
                                menor = min(cache_privada_instrucoes[processador].conjuntos[conjunto_privada], key=lambda l: l.contador)
                                menor.bloco = linha.bloco
                                menor.estado = 'S'
                                menor.contador = 1
                            break
                    if not hit:
                        print('Miss na cache compartilhada de instrucoes')
                        arq_log.write('Miss na cache compartilhada de instrucoes\n\n')
                        print('Buscando na memoria principal')
                        arq_log.write('Buscando na memoria principal\n\n')
                        bloco_memoria_principal = [hex(int(endereco, 16) - (int(endereco, 16) % TAMANHO_LINHA) + i) for i in range(TAMANHO_LINHA)]
                        # Insere o bloco na cache compartilhada
                        inserido = False
                        for linha_c in cache_compartilhada_instrucoes.conjuntos[conjunto_compartilhada]:
                            if linha_c.estado == 'I':
                                linha_c.bloco = bloco_memoria_principal
                                linha_c.estado = 'E'
                                linha_c.contador = 1
                                inserido = True
                                break
                        if not inserido:
                            menor = min(cache_compartilhada_instrucoes.conjuntos[conjunto_compartilhada], key=lambda l: l.contador)
                            menor.bloco = bloco_memoria_principal
                            menor.estado = 'E'
                            menor.contador = 1
                        # Insere o bloco na cache privada do processador atual
                        inserido = False
                        for linha_p in cache_privada_instrucoes[processador].conjuntos[conjunto_privada]:
                            if linha_p.estado == 'I':
                                linha_p.bloco = bloco_memoria_principal
                                linha_p.estado = 'E'
                                linha_p.contador = 1
                                inserido = True
                                break
                        if not inserido:
                            menor = min(cache_privada_instrucoes[processador].conjuntos[conjunto_privada], key=lambda l: l.contador)
                            menor.bloco = bloco_memoria_principal
                            menor.estado = 'E'
                            menor.contador = 1

            case 2:
                # Leitura de dados
                hit = False
                conjunto_privada = int(endereco, 16) % (NUMERO_LINHAS_CACHE_PRIVADA // NUMERO_LINHAS_CONJUNTO)
                # Verifica se há um hit na cache privada de dados
                for linha in cache_privada_dados[processador].conjuntos[conjunto_privada]:
                    if endereco in linha.bloco and linha.estado != 'I':
                        print('Hit na cache privada de dados')
                        arq_log.write('Hit na cache privada de dados\n\n')
                        hit = True
                        linha.contador += 1
                        break
                if not hit:
                    print('Miss na cache privada de dados')
                    arq_log.write('Miss na cache privada de dados\n\n')
                    conjunto_compartilhada = int(endereco, 16) % (NUMERO_LINHAS_CACHE_COMPARTILHADA // NUMERO_LINHAS_CONJUNTO)
                    # Verifica se há um hit na cache compartilhada de dados
                    for linha in cache_compartilhada_dados.conjuntos[conjunto_compartilhada]:
                        if endereco in linha.bloco and linha.estado != 'I':
                            print('Hit na cache compartilhada de dados')
                            arq_log.write('Hit na cache compartilhada de dados\n\n')
                            hit = True
                            linha.contador += 1
                            linha.estado = 'S'
                            # Atualiza o estado das linhas na cache privada de todos os processadores
                            for i in range(NUMERO_PROCESSADORES):
                                for linha_privada in cache_privada_dados[i].conjuntos[conjunto_privada]:
                                    if linha_privada.estado in ['M', 'E']:
                                        linha_privada.estado = 'S'
                            # Insere o bloco na cache privada do processador atual
                            inserido = False
                            for linha_p in cache_privada_dados[processador].conjuntos[conjunto_privada]:
                                if linha_p.estado == 'I':
                                    linha_p.bloco = linha.bloco
                                    linha_p.estado = 'S'
                                    linha_p.contador = 1
                                    inserido = True
                                    break
                            if not inserido:
                                menor = min(cache_privada_dados[processador].conjuntos[conjunto_privada], key=lambda l: l.contador)
                                menor.bloco = linha.bloco
                                menor.estado = 'S'
                                menor.contador = 1
                            break
                    if not hit:
                        print('Miss na cache compartilhada de dados')
                        arq_log.write('Miss na cache compartilhada de dados\n\n')
                        bloco_memoria_principal = [hex(int(endereco, 16) - (int(endereco, 16) % TAMANHO_LINHA) + i) for i in range(TAMANHO_LINHA)]
                        # Insere o bloco na cache compartilhada
                        inserido = False
                        for linha_c in cache_compartilhada_dados.conjuntos[conjunto_compartilhada]: 
                            if linha_c.estado == 'I':
                                linha_c.bloco = bloco_memoria_principal
                                linha_c.estado = 'E'
                                linha_c.contador = 1
                                inserido = True
                                break
                        if not inserido:
                            menor = min(cache_compartilhada_dados.conjuntos[conjunto_compartilhada], key=lambda l: l.contador)
                            menor.bloco = bloco_memoria_principal
                            menor.estado = 'E'
                            menor.contador = 1
                        # Insere o bloco na cache privada do processador atual
                        inserido = False
                        for linha_p in cache_privada_dados[processador].conjuntos[conjunto_privada]:
                            if linha_p.estado == 'I':
                                linha_p.bloco = bloco_memoria_principal
                                linha_p.estado = 'E'
                                linha_p.contador = 1
                                inserido = True
                                break
                        if not inserido:
                            menor = min(cache_privada_dados[processador].conjuntos[conjunto_privada], key=lambda l: l.contador)
                            menor.bloco = bloco_memoria_principal
                            menor.estado = 'E'
                            menor.contador = 1

            case 3:
                # Escrita de dados
                hit = False
                conjunto_privada = int(endereco, 16) % (NUMERO_LINHAS_CACHE_PRIVADA // NUMERO_LINHAS_CONJUNTO)
                # Verifica se há um hit na cache privada de dados
                for linha in cache_privada_dados[processador].conjuntos[conjunto_privada]:
                    if endereco in linha.bloco and linha.estado != 'I':
                        print('Hit na cache privada de dados')
                        arq_log.write('Hit na cache privada de dados\n\n')
                        hit = True
                        linha.contador += 1
                        linha.estado = 'M'
                        # Invalida o estado das linhas na cache privada de todos os processadores
                        for i in range(NUMERO_PROCESSADORES):
                            for linha_privada in cache_privada_dados[i].conjuntos[conjunto_privada]:
                                if endereco in linha_privada.bloco:
                                    linha_privada.estado = 'I'
                        # Invalida o estado das linhas na cache compartilhada
                        for linha_c in cache_compartilhada_dados.conjuntos[conjunto_privada]:
                            if endereco in linha_c.bloco:
                                linha_c.estado = 'I'
                        break
                if not hit:
                    print('Miss na cache privada de dados')
                    arq_log.write('Miss na cache privada de dados\n\n')
                    print('Buscando na cache compartilhada de dados')
                    arq_log.write('Buscando na cache compartilhada de dados\n\n')
                    conjunto_compartilhada = int(endereco, 16) % (NUMERO_LINHAS_CACHE_COMPARTILHADA // NUMERO_LINHAS_CONJUNTO)
                    # Verifica se há um hit na cache compartilhada de dados
                    for linha in cache_compartilhada_dados.conjuntos[conjunto_compartilhada]:
                        if endereco in linha.bloco and linha.estado != 'I':
                            print('Hit na cache compartilhada de dados')
                            arq_log.write('Hit na cache compartilhada de dados\n\n')
                            hit = True
                            linha.contador += 1
                            linha.estado = 'M'
                            # Invalida o estado das linhas na cache privada de todos os processadores
                            for i in range(NUMERO_PROCESSADORES):
                                for linha_privada in cache_privada_dados[i].conjuntos[conjunto_privada]:
                                    if endereco in linha_privada.bloco:
                                        linha_privada.estado = 'I'
                            # Invalida o estado das linhas na cache compartilhada
                            for linha_c in cache_compartilhada_dados.conjuntos[conjunto_privada]:
                                if endereco in linha_c.bloco:
                                    linha_c.estado = 'I'
                            # Insere o bloco na cache privada do processador atual
                            inserido = False
                            for linha_p in cache_privada_dados[processador].conjuntos[conjunto_privada]:
                                if linha_p.estado == 'I':
                                    linha_p.bloco = linha.bloco
                                    linha_p.estado = 'M'
                                    linha_p.contador = 1
                                    inserido = True
                                    break
                            if not inserido:
                                menor = min(cache_privada_dados[processador].conjuntos[conjunto_privada], key=lambda l: l.contador)
                                menor.bloco = linha.bloco
                                menor.estado = 'M'
                            break
                    if not hit:
                        print('Miss na cache compartilhada de dados')
                        arq_log.write('Miss na cache compartilhada de dados\n\n')
                        print('Buscando na memoria principal')
                        arq_log.write('Buscando na memoria principal\n\n')
                        bloco_memoria_principal = [hex(int(endereco, 16) - (int(endereco, 16) % TAMANHO_LINHA) + i) for i in range(TAMANHO_LINHA)]
                        # Insere o bloco na cache compartilhada
                        inserido = False
                        for linha_c in cache_compartilhada_dados.conjuntos[conjunto_compartilhada]:
                            if linha_c.estado == 'I':
                                linha_c.bloco = bloco_memoria_principal
                                linha_c.estado = 'M'
                                inserido = True
                                break
                        if not inserido:
                            menor = min(cache_compartilhada_dados.conjuntos[conjunto_compartilhada], key=lambda l: l.contador)
                            menor.bloco = bloco_memoria_principal
                            menor.estado = 'M'
                        # Insere o bloco na cache privada do processador atual
                        inserido = False
                        for linha_p in cache_privada_dados[processador].conjuntos[conjunto_privada]:
                            if linha_p.estado == 'I':
                                linha_p.bloco = bloco_memoria_principal
                                linha_p.estado = 'E'
                                linha_p.contador = 1
                                inserido = True
                                print(linha_p)
                                break
                        if not inserido:
                            menor = min(cache_privada_dados[processador].conjuntos[conjunto_privada], key=lambda l: l.contador)
                            menor.bloco = bloco_memoria_principal
                            menor.estado = 'E'
                            menor.contador = 1
        imprimir_caches(cache_privada_dados, cache_privada_instrucoes, cache_compartilhada_dados, cache_compartilhada_instrucoes, arq_log)
        instrucao_atual = instrucoes.readline()

if __name__ == '__main__':
    main()