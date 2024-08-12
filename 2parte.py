import tkinter as tk  
# Importa a biblioteca tkinter para a interface grafica
from tkinter import messagebox  
# Importa o widget de mensagem da tkinter
import random  
# Importa a biblioteca para gerar numeros aleatorios
import sys  
# Importa o sistema para manipular a entrada e saida

# Funcao para gerar o unigrama a partir das palavras fornecidas
def gerarUnigrama(palavra1, palavra2, palavra3):
    join = palavra1 + palavra2 + palavra3  
    # Junta as palavras em uma string
    unigram = ''.join(sorted(set(join), key=join.index))  
    # Remove caracteres duplicados e preserva a ordem
    if len(unigram) > 10:  
        # Verifica se o unigrama possui mais de 10 caracteres
        raise ValueError("Erro", "O resultado da palavra formada excede 10 caracteres.") 
    # Lanca um erro se o unigrama for invalido
    else:
        return unigram  # Retorna o unigrama

# Funcao para identificar as posicoes dos caracteres em uma palavra com base no unigrama
def identificar(w, unigram):
    posicoes = []  # Lista para armazenar as posicoes
    palavra = [char for char in w if char.isalpha()]  
    # Filtra apenas caracteres alfabeticos
    for letra in palavra:
# Itera sobre a lista 'unigram', obtendo tanto o índice (index) quanto o item (item) em cada iteracao
        for index, item in enumerate(unigram):  
            # Percorre o unigrama
            if letra == item:  
                # Verifica se o caractere esta no unigrama
                posicoes.append(index)  
                # Adiciona a posicao correspondente
    return posicoes  # Retorna a lista de posicoes

# Funcao para gerar vetores aleatorios
def gerarVetores(num_vetores, tamanho_vetor, num_range=10):
    vetores = [] 
    # Lista para armazenar os vetores
    for _ in range(num_vetores):
        vetor = random.sample(range(num_range), tamanho_vetor)  
        # Gera um vetor aleatorio
        vetores.append(vetor)  
        # Adiciona o vetor a lista
    return vetores  # Retorna a lista de vetores

# Funcao para converter um vetor em um inteiro com base nas posicoes fornecidas
def converterParaInt(vetor, posicoes):
    digitos_selecionados = [vetor[pos] for pos in posicoes]  
    # Seleciona os digitos baseados nas posicoes
    concatenado_str = ''.join(map(str, digitos_selecionados))  
    # Concatena os digitos em uma string
    resultadoInt = int(concatenado_str)  
    # Converte a string em um inteiro
    return resultadoInt  # Retorna o inteiro resultante

# Funcao para realizar a mutacao em um vetor
def mutacao(vetor):
    vetor_copia = vetor.copy()  
    # Faz uma copia do vetor
    i, j = random.sample(range(len(vetor_copia)), 2)  
    # Seleciona dois indices aleatorios
    vetor_copia[i], vetor_copia[j] = vetor_copia[j], vetor_copia[i]  
    # Troca os elementos nos indices
    return vetor_copia  # Retorna o vetor mutado

# Funcao para calcular o fitness dos vetores com base nas palavras e no unigrama
def fitness(vetores, palavra1, palavra2, palavra3, unigram, imprimir):
    vetorpalavra1 = identificar(palavra1, unigram)  # Identifica as posicoes para a palavra 1
    vetorpalavra2 = identificar(palavra2, unigram)  # Identifica as posicoes para a palavra 2
    vetorpalavra3 = identificar(palavra3, unigram)  # Identifica as posicoes para a palavra 3

    resultados = []  # Lista para armazenar os resultados

    for idx, vetor in enumerate(vetores):
        palavra1 = converterParaInt(vetor, vetorpalavra1)  # Converte o vetor para a palavra 1
        palavra2 = converterParaInt(vetor, vetorpalavra2)  # Converte o vetor para a palavra 2
        palavra3 = converterParaInt(vetor, vetorpalavra3)  # Converte o vetor para a palavra 3
        fitnessVetor = palavra3 - (palavra1 + palavra2)  # Calcula o fitness do vetor
    
        resultados.append((fitnessVetor, vetor))  
        # Adiciona o resultado a lista
    
    resultadosOrdenados = sorted(resultados, key=lambda x: abs(x[0]))  
    # Ordena os resultados pelo valor absoluto do fitness
    if imprimir == 1:
# Itera sobre a lista 'resultadosOrdenados', obtendo o indice (idx), 
# o valor de fitness (fitnessVetor) e o vetor em cada iteracao, iniciando o indice em 1
        for idx, (fitnessVetor, vetor) in enumerate(resultadosOrdenados, start=1):
            print(f"Vetor {idx}: {vetor} Fitness: {fitnessVetor}")  
            # Imprime o vetor e seu fitness
    
    return resultadosOrdenados  # Retorna os resultados ordenados

# Funcao para realizar a selecao por torneio
# 'tamanho_torneio' define quantos candidatos serao comparados em cada torneio (padrao e 3)
def torneio(vetores, tamanho_torneio=3):
    pais_selecionados = []  
    # Lista para armazenar os pais selecionados

    for _ in range(len(vetores)):
        competidores = random.sample(vetores, tamanho_torneio)  # Seleciona competidores aleatorios
        melhor = min(competidores, key=lambda x: abs(x[0]))  # Encontra o melhor competidor
        pais_selecionados.append(melhor[1])  # Adiciona o vetor do melhor competidor
    return pais_selecionados  # Retorna os pais selecionados

# Funcao para realizar a selecao por roleta
def roleta(vetores):
    if not vetores:
        return []
    
    aptidoes, individuos = zip(*vetores)  # Separa aptidoes e individuos
    aptidao_total = sum(aptidoes)  # Calcula o total das aptidoes
    probabilidades = [apt / aptidao_total for apt in aptidoes]  # Calcula as probabilidades
    
    limites_acumulados = []  # Lista para armazenar os limites acumulados
    acumulado = 0
    for prob in probabilidades:
        acumulado += prob
        limites_acumulados.append(acumulado)  # Adiciona o limite acumulado
    
    pais_selecionados = []  # Lista para armazenar os pais selecionados
    for _ in range(len(vetores)):
        r = random.random()  # Gera um numero aleatorio
# Itera sobre a lista 'limites_acumulados', enumerate obtendo o indice (i) e o valor de limite em cada iteracao
        for i, limite in enumerate(limites_acumulados):
            if r <= limite:  # Verifica em qual limite o numero aleatorio se encaixa
                pais_selecionados.append(individuos[i])  # Adiciona o individuo correspondente
                break
    return pais_selecionados  # Retorna os pais selecionados

# Funcao para aplicar a mutacao nos vetores com base na taxa de mutacao
def mutacaoFitness(vetores, taxaMutacao):
    indicesMutacao = []  # Lista para armazenar os indices de mutacao
    taxaMutacao = round((taxaMutacao * len(vetores)) / 100)  # Calcula o numero de vetores a serem mutados
    indicesMutacao = random.sample(range(len(vetores)), taxaMutacao)#Seleciona indices aleatorios para mutacao
    for index in indicesMutacao:
        vetores[index] = mutacao(vetores[index])  # Aplica a mutacao
    return vetores  # Retorna os vetores com mutacao

# Funcao para aplicar o crossover ciclico nos pais selecionados
def crossoverCiclo(pais, taxaCrossover):
    filhos = []  # Lista para armazenar os filhos

    for i in range(0, len(pais) - 1, 2):
        if random.random() < taxaCrossover:
            pai1 = pais[i]  # Seleciona o primeiro pai
            pai2 = pais[i + 1]  # Seleciona o segundo pai
            filho1 = pai1.copy()  # Cria uma copia do primeiro pai
            filho2 = pai2.copy()  # Cria uma copia do segundo pai
            
            ciclo = [0]  # Inicializa o ciclo com o primeiro elemento
            while True:
                idx = ciclo[-1]
                if pai2[idx] in pai1:  # Verifica se o elemento esta no pai1
                    idx = pai1.index(pai2[idx])  # Encontra o indice correspondente no pai1
                    if idx in ciclo:
                        break
                    ciclo.append(idx)  # Adiciona o indice ao ciclo
                else:
                    break
            
            for idx in ciclo:
                filho1[idx], filho2[idx] = filho2[idx], filho1[idx]  # Troca os elementos nos indices do ciclo
            
            filhos.append(filho1)  # Adiciona o primeiro filho
            filhos.append(filho2)  # Adiciona o segundo filho
        else:
            filhos.append(pais[i].copy())  # Sem crossover, adiciona uma copia do pai1
            filhos.append(pais[i + 1].copy())  # Sem crossover, adiciona uma copia do pai2
    
    return filhos  # Retorna os filhos gerados

# Funcao para aplicar o crossover PMX nos pais
def pmxCrossover(pai1, pai2):
    tamanho = len(pai1)  # Obtém o tamanho do vetor
    pontos_crossover = sorted(random.sample(range(tamanho), 2))  # Seleciona pontos de crossover aleatorios
    inicio_crossover, fim_crossover = pontos_crossover[0], pontos_crossover[1]

    filho1, filho2 = pai1[:], pai2[:]  # Cria copias dos pais

    mapeamento1 = {}  # Dicionario para armazenar o mapeamento para o filho1
    mapeamento2 = {}  # Dicionario para armazenar o mapeamento para o filho2

    for i in range(inicio_crossover, fim_crossover):
        filho1[i] = pai2[i]  # Preenche o filho1 com os elementos do pai2
        filho2[i] = pai1[i]  # Preenche o filho2 com os elementos do pai1
        mapeamento1[pai2[i]] = pai1[i]  # Adiciona o mapeamento para o filho1
        mapeamento2[pai1[i]] = pai2[i]  # Adiciona o mapeamento para o filho2

    def reparar(child, mapeamento):
        for i in range(tamanho):
            if i < inicio_crossover or i >= fim_crossover:
                while child[i] in mapeamento:
                    child[i] = mapeamento[child[i]]  # Substitui elementos duplicados

    reparar(filho1, mapeamento1)  # Repara o filho1
    reparar(filho2, mapeamento2)  # Repara o filho2

    return filho1, filho2  # Retorna os filhos gerados

# Funcao para realizar o crossover da populacao selecionada
def crossoverPopulacao(pais_selecionados, taxaCrossover):
    proxima_geracao = []  # Lista para armazenar a proxima geracao
    for i in range(0, len(pais_selecionados), 2):
        if i+1 < len(pais_selecionados):
            pai1 = pais_selecionados[i]  # Seleciona o primeiro pai
            pai2 = pais_selecionados[i + 1]  # Seleciona o segundo pai
            if random.random() < taxaCrossover:
                filho1, filho2 = pmxCrossover(pai1, pai2)  # Aplica o crossover PMX
            else:
                filho1, filho2 = pai1[:], pai2[:]  # Sem crossover, os filhos sao copias dos pais
            proxima_geracao.extend([filho1, filho2])  # Adiciona os filhos a proxima geracao
    return proxima_geracao  # Retorna a proxima geracao

# Funcao principal para executar o algoritmo genetico e salvar a resultado em um arquivo
def executarAlgoritmo(numerovetor, geracoes, taxaMutacao, palavra1, palavra2, palavra3, unigram, tamanho, crossover, selecao):
    vetores = gerarVetores(numerovetor, tamanho)  # Gera os vetores iniciais
    original_stdout = sys.stdout  # Salva a referencia da resultado padrao original
    with open("resultado.txt", "w") as f:
        sys.stdout = f  # Redireciona a resultado para o arquivo
        if crossover == 2:
            print("\n---Fitness Inicial---\n")  # Imprime a header para o fitness inicial
            fitness(vetores, palavra1, palavra2, palavra3, unigram, imprimir=1)  
            # Calcula e imprime o fitness inicial
            for i in range(geracoes):
                vetores_mutados = mutacaoFitness(vetores, taxaMutacao)  # Aplica mutacao nos vetores
                vetores_ordenados = fitness(vetores_mutados, palavra1, palavra2, palavra3, unigram, imprimir=0)  
                # Calcula o fitness dos vetores mutados
                if selecao == 2:
                    pais = torneio(vetores_ordenados, tamanho_torneio=3)  # Seleciona pais por torneio
                    filhos = crossoverCiclo(pais, taxaCrossover=0.6)  # Aplica o crossover ciclico
                    print("\nNumero da Geracao.", i + 1, "\n")  # Imprime o numero da geracao
                    fitness(filhos, palavra1, palavra2, palavra3, unigram, imprimir=1)  
                    # Calcula e imprime o fitness da nova geracao
                elif selecao == 1:
                    pais = roleta(vetores_ordenados)  # Seleciona pais por roleta
                    filhos = crossoverCiclo(pais, taxaCrossover=0.8)  # Aplica o crossover ciclico
                    print("\nNumero da Geracao.", i + 1, "\n")  # Imprime o numero da geracao
                    fitness(filhos, palavra1, palavra2, palavra3, unigram, imprimir=1)  
                    # Calcula e imprime o fitness da nova geracao
        elif crossover == 1:
            print("\n---Fitness Inicial---\n")  # Imprime a header para o fitness inicial
            fitness(vetores, palavra1, palavra2, palavra3, unigram, imprimir=1)  # Calcula e imprime o fitness inicial
            for i in range(geracoes):
                vetores_mutados = mutacaoFitness(vetores, taxaMutacao)  # Aplica mutacao nos vetores
                vetores_ordenados = fitness(vetores_mutados, palavra1, palavra2, palavra3, unigram, imprimir=0)  
                # Calcula o fitness dos vetores mutados
                if selecao == 2:
                    pais = torneio(vetores_ordenados, tamanho_torneio=3)  # Seleciona pais por torneio
                    filhos = crossoverPopulacao(pais, taxaCrossover=0.1)  # Aplica o crossover na populacao
                    print("\nNumero da Geracao.", i + 1, "\n")  # Imprime o numero da geracao
                    fitness(filhos, palavra1, palavra2, palavra3, unigram, imprimir=1) 
                    # Calcula e imprime o fitness da nova geracao
                elif selecao == 1:
                    pais = roleta(vetores_ordenados)  # Seleciona pais por roleta
                    filhos = crossoverPopulacao(pais, taxaCrossover=0.05)  # Aplica o crossover na populacao
                    print("\nNumero da Geracao.", i + 1, "\n")  # Imprime o numero da geracao
                    fitness(filhos, palavra1, palavra2, palavra3, unigram, imprimir=1)  
                    # Calcula e imprime o fitness da nova geracao
    
    sys.stdout = original_stdout  # Restaura a saida padrao original

# Funcao para executar o algoritmo a partir da interface grafica
def executar_algoritmo():
    try:
        palavra1 = entry_word1.get()  
        # Obtém a palavra 1 do input
        palavra2 = entry_word2.get()  
        # Obtém a palavra 2 do input
        palavra3 = entry_word3.get()  
        # Obtém a palavra 3 do input
        taxa_mutacao = int(entry_mutation_rate.get())  
        # Obtém a taxa de mutacao do input
        numerovetor = int(entry_numerovetortors.get())  
        # Obtém o numero de vetores do input
        geracoes = int(entry_generations.get())  
        # Obtém o numero de geracoes do input

        unigram = gerarUnigrama(palavra1, palavra2, palavra3) 
        # Gera o unigrama,"unigram" considera apenas palavras isoladas sem levar em conta o contexto das palavras vizinhas.
        tamanho = len(unigram)  
        # Calcula o tamanho do unigrama

        crossover = int(crossover_var.get())  
        # Obtém o metodo de crossover selecionado
        selecao = int(selection_var.get())  
        # Obtém o metodo de selecao selecionado

        executarAlgoritmo(numerovetor, geracoes, taxa_mutacao, palavra1, palavra2, palavra3, unigram, tamanho, crossover, selecao)  
        # Executa o algoritmo
        messagebox.showinfo("Info", "Algoritmo concluido. Verifique o arquivo 'saida.txt'.")  
        # Exibe mensagem de sucesso

    except ValueError as e:
        messagebox.showerror("Erro", str(e))  
        # Exibe mensagem de erro se ocorrer uma excecao

# Configuracao da janela principal
root = tk.Tk()  
# Cria a janela principal
root.title("Configuracao do Algoritmo Genetico")  
# Define o titulo da janela

# Criacao dos widgets
tk.Label(root, text="Palavra 1:").grid(row=0, column=0, padx=10, pady=5)  
# Label para a palavra 1
entry_word1 = tk.Entry(root)  
# Campo de entrada para a palavra 1
entry_word1.grid(row=0, column=1, padx=10, pady=5)  
# Posiciona o campo de entrada

tk.Label(root, text="Palavra 2:").grid(row=1, column=0, padx=10, pady=5)  
# Label para a palavra 2
entry_word2 = tk.Entry(root)  
# Campo de entrada para a palavra 2
entry_word2.grid(row=1, column=1, padx=10, pady=5)  
# Posiciona o campo de entrada

tk.Label(root, text="Palavra 3:").grid(row=2, column=0, padx=10, pady=5) 
# Label para a palavra 3
entry_word3 = tk.Entry(root) 
# Campo de entrada para a palavra 3
entry_word3.grid(row=2, column=1, padx=10, pady=5)  
# Posiciona o campo de entrada

tk.Label(root, text="Taxa de Mutacao (%):").grid(row=3, column=0, padx=10, pady=5)  
# Label para a taxa de mutacao
entry_mutation_rate = tk.Entry(root) 
# Campo de entrada para a taxa de mutacao
entry_mutation_rate.grid(row=3, column=1, padx=10, pady=5)  
# Posiciona o campo de entrada

tk.Label(root, text="Numero de Vetores:").grid(row=4, column=0, padx=10, pady=5)  
# Label para o numero de vetores
entry_numerovetortors = tk.Entry(root)  
# Campo de entrada para o numero de vetores
entry_numerovetortors.grid(row=4, column=1, padx=10, pady=5)  
# Posiciona o campo de entrada

tk.Label(root, text="Numero de Geracoes:").grid(row=5, column=0, padx=10, pady=5)  
# Label para o numero de geracoes
entry_generations = tk.Entry(root)  
# Campo de entrada para o numero de geracoes
entry_generations.grid(row=5, column=1, padx=10, pady=5)  
# Posiciona o campo de entrada

tk.Label(root, text="Metodo de Crossover:").grid(row=6, column=0, padx=10, pady=5)  # Label para o metodo de crossover
crossover_var = tk.StringVar(value="1") 
# Variavel para armazenar o metodo de crossover
tk.Radiobutton(root, text="PMX", variable=crossover_var, value="1").grid(row=6, column=1, padx=10, pady=5)  
# Botao de opcao PMX
tk.Radiobutton(root, text="Ciclico", variable=crossover_var, value="2").grid(row=6, column=2, padx=10, pady=5)  
# Botao de opcao Ciclico

tk.Label(root, text="Metodo de Selecao:").grid(row=7, column=0, padx=10, pady=5)  
# Label para o metodo de selecao
selection_var = tk.StringVar(value="1")  
# Variavel para armazenar o metodo de selecao
tk.Radiobutton(root, text="Roleta", variable=selection_var, value="1").grid(row=7, column=1, padx=10, pady=5) 
# Botao de opcao Roleta
tk.Radiobutton(root, text="Torneio", variable=selection_var, value="2").grid(row=7, column=2, padx=10, pady=5)  
# Botao de opcao Torneio

tk.Button(root, text="Executar Algoritmo", command=executar_algoritmo).grid(row=8, column=0, columnspan=3, padx=10, pady=10) 
# Botao para executar o algoritmo

root.mainloop() 
# Inicia a interface grafica
