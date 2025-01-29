import config
import sys

# Lorenzo Henrique Zanetti - RA: 133076
# Lucas de Oliveira Fratus - RA: 134698
# Matheus Jacomini Cenerini - RA: 134700

class LinhaCache:
    def __init__(self):
        self.bloco = []
        self.contador = -1
        self.estado = 'I'

    def __str__(self):
        return f'Est: {self.estado} - Bloco: {self.bloco}'


class LinhaCacheCompartilhada:
    def __init__(self):
        self.bloco = []
        self.contador = -1

    def __str__(self):
        return f'Bloco: {self.bloco}'


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


class CacheCompartilhada:
    def __init__(self, n_linhas, n_linhas_por_conjunto):
        self.conjuntos = {}
        for i in range(n_linhas//n_linhas_por_conjunto):
            self.conjuntos[i] = [LinhaCacheCompartilhada() for j in range(n_linhas_por_conjunto)]
    
    def __str__(self):
        retorno = ''
        for conjunto in self.conjuntos:
            retorno += f'Conjunto {conjunto}:\n'
            for linha in self.conjuntos[conjunto]:
                retorno += f'{linha}\n'
            retorno += '\n'
        return retorno


def imprimir_caches(cache_privada_dados, cache_privada_instrucoes, cache_compartilhada_dados, cache_compartilhada_instrucoes, arq_log):
    arq_log.write('################## Cache privada de dados ##################\n\n')
    for i in range(len(cache_privada_dados)):
        arq_log.write(f'Processador {i}:\n\n')
        arq_log.write(str(cache_privada_dados[i]))
    arq_log.write('################## Cache privada de instrucoes ##################\n\n')
    for i in range(len(cache_privada_instrucoes)):
        arq_log.write(f'Processador {i}:\n\n')
        arq_log.write(str(cache_privada_instrucoes[i]))
    arq_log.write('~~~~~~~~~~~~~~~~~~ Cache compartilhada de dados ~~~~~~~~~~~~~~~~~~\n\n')
    arq_log.write(str(cache_compartilhada_dados))
    arq_log.write('~~~~~~~~~~~~~~~~~~ Cache compartilhada de instrucoes ~~~~~~~~~~~~~~~~~~\n\n')
    arq_log.write(str(cache_compartilhada_instrucoes))
    arq_log.write('\n--------------------------------------------------------------------------------------------\n')


def separa_instrucao(instrucao: str) -> tuple:
    instrucao = instrucao.split()
    return (int(instrucao[0]), int(instrucao[1]), '0x' + str(instrucao[2]))


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

    if NUMERO_LINHAS_CACHE_PRIVADA * NUMERO_PROCESSADORES > NUMERO_LINHAS_CACHE_COMPARTILHADA:
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


def main(nome_arq_instrucoes: str):
    arq_log = open('log.txt', 'w')
    leitura_arquivo_configuracao()
    arq_log.write(f'Numero de processadores: {NUMERO_PROCESSADORES}\n')
    arq_log.write(f'Tamanho da linha: {TAMANHO_LINHA}\n')
    arq_log.write(f'Numero de linhas da cache compartilhada: {NUMERO_LINHAS_CACHE_COMPARTILHADA}\n')
    arq_log.write(f'Numero de linhas da cache privada: {NUMERO_LINHAS_CACHE_PRIVADA}\n')
    arq_log.write(f'Numero de linhas por conjunto: {NUMERO_LINHAS_CONJUNTO}\n')

    cache_compartilhada_dados = CacheCompartilhada(NUMERO_LINHAS_CACHE_COMPARTILHADA, NUMERO_LINHAS_CONJUNTO)
    cache_compartilhada_instrucoes = CacheCompartilhada(NUMERO_LINHAS_CACHE_COMPARTILHADA, NUMERO_LINHAS_CONJUNTO) 

    cache_privada_dados = []
    cache_privada_instrucoes = []
    for i in range(NUMERO_PROCESSADORES):
        cache_privada_dados.append(Cache(NUMERO_LINHAS_CACHE_PRIVADA, NUMERO_LINHAS_CONJUNTO))
        cache_privada_instrucoes.append(Cache(NUMERO_LINHAS_CACHE_PRIVADA, NUMERO_LINHAS_CONJUNTO))


    arq_instrucoes = open(nome_arq_instrucoes, 'r')

    MESI(cache_privada_dados, cache_privada_instrucoes, cache_compartilhada_dados, cache_compartilhada_instrucoes, arq_instrucoes, arq_log)

    arq_instrucoes.close()


def MESI(cache_privada_dados, cache_privada_instrucoes, cache_compartilhada_dados, cache_compartilhada_instrucoes, instrucoes, arq_log):
    instrucao_atual = instrucoes.readline()
    while instrucao_atual:
        processador, operacao, endereco = separa_instrucao(instrucao_atual)
        if processador >= NUMERO_PROCESSADORES:
            raise ValueError('O id do processador não pode ser maior que o número de processadores.')
        elif operacao not in [0, 2, 3]:
            raise ValueError('O tipo de operação deve ser 0, 2 ou 3.')
        elif len(endereco) != 10: # 10 caracteres = 4 bytes + 2 caracteres de espaço
            raise ValueError('O endereço deve ter 8 caracteres (4 bytes).')
        
        arq_log.write(f'Processador: {processador} - Operacao: {operacao} - Endereco: {endereco}\n')

        #   bloco = endereco // N_LINHAS_BLOCO (tamanho da linha)
        #   conjunto = bloco % N_CONJUNTOS
        bloco = int(endereco, 16) // TAMANHO_LINHA
        conjunto_privada = bloco % (NUMERO_LINHAS_CACHE_PRIVADA // NUMERO_LINHAS_CONJUNTO)
        conjunto_compartilhada = bloco % (NUMERO_LINHAS_CACHE_COMPARTILHADA // NUMERO_LINHAS_CONJUNTO)

        match operacao:
            case 0:
                # Leitura de instrucoes
                hit = False
                # Verifica se há um hit na cache privada de instruções
                for linha in cache_privada_instrucoes[processador].conjuntos[conjunto_privada]: # tentar encontrar o bloco em seu respectivo conjunto
                    if endereco in linha.bloco and linha.estado != 'I':
                        arq_log.write('Read Hit na cache privada de instrucoes\n\n')
                        hit = True
                        if POLITICA_SUBSTITUICAO == 'LFU':
                            linha.contador += 1
                        break
                if not hit:
                    arq_log.write('Read Miss na cache privada de instrucoes\n\n')
                    arq_log.write('Buscando na cache compartilhada de instrucoes\n\n')
                    # Verifica se há um hit na cache compartilhada de instruções
                    for linha_sh in cache_compartilhada_instrucoes.conjuntos[conjunto_compartilhada]:
                        if endereco in linha_sh.bloco:
                            arq_log.write('Hit na cache compartilhada de instrucoes\n\n')
                            hit = True
                            if POLITICA_SUBSTITUICAO == 'LFU':
                                linha_sh.contador += 1
                            # Atualiza o estado das linhas na cache privada de todos os processadores
                            for i in range(NUMERO_PROCESSADORES):
                                for linha_privada in cache_privada_instrucoes[i].conjuntos[conjunto_privada]:
                                    if linha_privada.estado in ['M', 'E']:
                                        linha_privada.estado = 'S'
                            # Insere o bloco na cache privada do processador atual
                            inserido = False
                            if POLITICA_SUBSTITUICAO == 'LFU':
                                for linha_p in cache_privada_instrucoes[processador].conjuntos[conjunto_privada]:
                                    if linha_p.estado == 'I':
                                        linha_p.bloco = linha_sh.bloco
                                        linha_p.estado = 'S'
                                        linha_p.contador = 1
                                        inserido = True
                                        break
                                if not inserido:
                                    menor = min(cache_privada_instrucoes[processador].conjuntos[conjunto_privada], key=lambda l: l.contador)
                                    menor.bloco = linha_sh.bloco
                                    menor.estado = 'S'
                                    menor.contador = 1
                            else: # FIFO
                                for linha_p in cache_privada_instrucoes[processador].conjuntos[conjunto_privada]:
                                    linha_p.contador += 1
                                    if linha_p.estado == 'I' and inserido == False:
                                        linha_p.bloco = linha_sh.bloco
                                        linha_p.estado = 'S'
                                        linha_p.contador = 0
                                        inserido = True
                                if not inserido:
                                    maior = max(cache_privada_instrucoes[processador].conjuntos[conjunto_privada], key=lambda l: l.contador)
                                    maior.bloco = linha_sh.bloco
                                    maior.estado = 'S'
                                    maior.contador = 0
                            break
                    if not hit:
                        arq_log.write('Miss na cache compartilhada de instrucoes\n\n')
                        arq_log.write('Buscando na memoria principal\n\n')
                        bloco_memoria_principal = [hex(int(endereco, 16) - (int(endereco, 16) % TAMANHO_LINHA) + i) for i in range(TAMANHO_LINHA)]
                        
                        # Insere o bloco na cache compartilhada
                        inserido = False
                        if POLITICA_SUBSTITUICAO == 'LFU':
                            for linha_c in cache_compartilhada_instrucoes.conjuntos[conjunto_compartilhada]:
                                if linha_c.bloco == []:
                                    linha_c.bloco = bloco_memoria_principal
                                    linha_c.contador = 1
                                    inserido = True
                                    break
                            if not inserido:
                                menor = min(cache_compartilhada_instrucoes.conjuntos[conjunto_compartilhada], key=lambda l: l.contador)
                                menor.bloco = bloco_memoria_principal
                                menor.contador = 1
                        else: # FIFO
                            for linha_c in cache_compartilhada_instrucoes.conjuntos[conjunto_compartilhada]:
                                linha_c.contador += 1
                                if inserido == False and linha_c.bloco == []:
                                    linha_c.bloco = bloco_memoria_principal
                                    linha_c.contador = 0
                                    inserido = True
                            if not inserido:
                                maior = max(cache_compartilhada_instrucoes.conjuntos[conjunto_compartilhada], key=lambda l: l.contador)
                                maior.bloco = bloco_memoria_principal
                                maior.contador = 0

                        # Insere o bloco na cache privada do processador atual
                        inserido = False
                        if POLITICA_SUBSTITUICAO == 'LFU':
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
                        else: # FIFO
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

                # Verifica se há um hit na cache privada de dados
                for linha in cache_privada_dados[processador].conjuntos[conjunto_privada]:
                    if endereco in linha.bloco and linha.estado != 'I':
                        arq_log.write('Read Hit na cache privada de dados\n\n')
                        hit = True
                        if POLITICA_SUBSTITUICAO == 'LFU':
                            linha.contador += 1
                        break

                if not hit:
                    arq_log.write('Read Miss na cache privada de dados\n\n')
                    arq_log.write('Buscando na cache compartilhada de dados\n\n')

                    # Verifica se há um hit na cache compartilhada de dados
                    for linha in cache_compartilhada_dados.conjuntos[conjunto_compartilhada]:
                        if endereco in linha.bloco:
                            arq_log.write('Hit na cache compartilhada de dados\n\n')
                            hit = True

                            if POLITICA_SUBSTITUICAO == 'LFU':
                                linha.contador += 1

                            # Atualiza o estado das linhas na cache privada de todos os processadores
                            for i in range(NUMERO_PROCESSADORES):
                                for linha_privada in cache_privada_dados[i].conjuntos[conjunto_privada]:
                                    if linha_privada.estado in ['M', 'E']:
                                        linha_privada.estado = 'S'

                            # Insere o bloco na cache privada do processador atual
                            inserido = False
                            if POLITICA_SUBSTITUICAO == 'LFU':
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

                            else: # FIFO
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
                        arq_log.write('Miss na cache compartilhada de dados\n\n')
                        arq_log.write('Buscando na memoria principal\n\n')
                        bloco_memoria_principal = [hex(int(endereco, 16) - (int(endereco, 16) % TAMANHO_LINHA) + i) for i in range(TAMANHO_LINHA)]
                        
                        # Insere o bloco na cache compartilhada
                        inserido = False
                        if POLITICA_SUBSTITUICAO == 'LFU':
                            for linha_c in cache_compartilhada_dados.conjuntos[conjunto_compartilhada]: 
                                if linha_c.bloco == []:
                                    linha_c.bloco = bloco_memoria_principal
                                    linha_c.contador = 1
                                    inserido = True
                                    break
                            if not inserido:
                                menor = min(cache_compartilhada_dados.conjuntos[conjunto_compartilhada], key=lambda l: l.contador)
                                menor.bloco = bloco_memoria_principal
                                menor.contador = 1
                        else:
                            for linha_c in cache_compartilhada_dados.conjuntos[conjunto_compartilhada]:
                                linha_c.contador += 1
                                if inserido == False and linha_c.bloco == []:
                                    linha_c.bloco = bloco_memoria_principal
                                    linha_c.contador = 0
                                    inserido = True
                            if not inserido:
                                maior = max(cache_compartilhada_dados.conjuntos[conjunto_compartilhada], key=lambda l: l.contador)
                                maior.bloco = bloco_memoria_principal
                                maior.contador = 0

                        # Insere o bloco na cache privada do processador atual
                        inserido = False
                        if POLITICA_SUBSTITUICAO == 'LFU':
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
                        else:
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
                # Verifica se há um hit na cache privada de dados
                for linha in cache_privada_dados[processador].conjuntos[conjunto_privada]:
                    if endereco in linha.bloco and linha.estado != 'I':
                        arq_log.write('Write Hit na cache privada de dados\n\n')
                        hit = True
                        if POLITICA_SUBSTITUICAO == 'LFU':
                            linha.contador += 1
                        # Invalida o estado das linhas na cache privada de todos os processadores
                        for i in range(NUMERO_PROCESSADORES):
                            for linha_privada in cache_privada_dados[i].conjuntos[conjunto_privada]:
                                if endereco in linha_privada.bloco:
                                    linha_privada.estado = 'I'
                        linha.estado = 'M'
                        break

                if not hit:
                    arq_log.write('Write Miss na cache privada de dados\n\n')
                    arq_log.write('Buscando na cache compartilhada de dados\n\n')
                    # Verifica se há um hit na cache compartilhada de dados
                    for linha in cache_compartilhada_dados.conjuntos[conjunto_compartilhada]:
                        if endereco in linha.bloco:
                            hit = True

                            # Invalida o estado das linhas na cache privada de todos os processadores
                            for i in range(NUMERO_PROCESSADORES):
                                for linha_privada in cache_privada_dados[i].conjuntos[conjunto_privada]:
                                    if endereco in linha_privada.bloco:
                                        linha_privada.estado = 'I'

                            # Insere o bloco na cache privada do processador atual
                            inserido = False
                            if POLITICA_SUBSTITUICAO == 'LFU':
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
                                    menor.contador = 1
                            else: # FIFO
                                for linha_p in cache_privada_dados[processador].conjuntos[conjunto_privada]:
                                    if linha_p.estado == 'I' and inserido == False:
                                        linha_p.bloco = linha.bloco
                                        linha_p.estado = 'M'
                                        linha_p.contador = 0
                                        inserido = True
                                if not inserido:
                                    maior = max(cache_privada_dados[processador].conjuntos[conjunto_privada], key=lambda l: l.contador)
                                    maior.bloco = linha.bloco
                                    maior.estado = 'M'
                                    maior.contador = 0
                            break

                    if not hit:
                        arq_log.write('Miss na cache compartilhada de dados\n\n')
                        arq_log.write('Buscando na memoria principal\n\n')
                        bloco_memoria_principal = [hex(int(endereco, 16) - (int(endereco, 16) % TAMANHO_LINHA) + i) for i in range(TAMANHO_LINHA)]
                        
                        # Insere o bloco na cache compartilhada
                        inserido = False
                        if POLITICA_SUBSTITUICAO == 'LFU':
                            for linha_c in cache_compartilhada_dados.conjuntos[conjunto_compartilhada]:
                                if linha_c.bloco == []:
                                    linha_c.bloco = bloco_memoria_principal
                                    linha_c.contador = 1
                                    inserido = True
                                    break
                            if not inserido:
                                menor = min(cache_compartilhada_dados.conjuntos[conjunto_compartilhada], key=lambda l: l.contador)
                                menor.bloco = bloco_memoria_principal
                                menor.contador = 1
                        else: # FIFO
                            for linha_c in cache_compartilhada_dados.conjuntos[conjunto_compartilhada]:
                                linha_c.contador += 1
                                if inserido == False and linha_c.bloco == []:
                                    linha_c.bloco = bloco_memoria_principal
                                    linha_c.contador = 0
                                    inserido = True
                            if not inserido:
                                maior = max(cache_compartilhada_dados.conjuntos[conjunto_compartilhada], key=lambda l: l.contador)
                                maior.bloco = bloco_memoria_principal
                                maior.contador = 0

                        # Insere o bloco na cache privada do processador atual
                        inserido = False

                        if POLITICA_SUBSTITUICAO == 'LFU':
                            for linha_p in cache_privada_dados[processador].conjuntos[conjunto_privada]:
                                if linha_p.estado == 'I':
                                    linha_p.bloco = bloco_memoria_principal
                                    linha_p.estado = 'M'
                                    linha_p.contador = 1
                                    inserido = True
                                    break
                            if not inserido:
                                menor = min(cache_privada_dados[processador].conjuntos[conjunto_privada], key=lambda l: l.contador)
                                menor.bloco = bloco_memoria_principal
                                menor.estado = 'M'
                                menor.contador = 1
                        else: # FIFO
                            for linha_p in cache_privada_dados[processador].conjuntos[conjunto_privada]:
                                linha_p.contador += 1
                                if linha_p.estado == 'I' and inserido == False:
                                    linha_p.bloco = bloco_memoria_principal
                                    linha_p.estado = 'M'
                                    linha_p.contador = 0
                                    inserido = True
                            if not inserido:
                                maior = max(cache_privada_dados[processador].conjuntos[conjunto_privada], key=lambda l: l.contador)
                                maior.bloco = bloco_memoria_principal
                                maior.estado = 'M'
                                maior.contador = 0
        imprimir_caches(cache_privada_dados, cache_privada_instrucoes, cache_compartilhada_dados, cache_compartilhada_instrucoes, arq_log)
        instrucao_atual = instrucoes.readline()

if __name__ == '__main__':
    '''
    Formato da commandline:
    python main.py <nome_arquivo_instrucoes>
    O log será gerado como log.txt
    '''
    if len(sys.argv) != 2:
        raise ValueError('O programa deve ser executado com o nome do arquivo de instruções.')
    main(sys.argv[1])