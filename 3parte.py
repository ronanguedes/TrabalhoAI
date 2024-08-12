import numpy as np
import tkinter as tk
from tkinter import messagebox
import random
import time

# Função para obter letras únicas de três palavras
def letras_unicas(palavras):
    todas_letras = ''.join(palavras)
    letras_unicas = ''.join(sorted(set(todas_letras), key=todas_letras.index))
    return letras_unicas

# Função para obter os índices das letras nas palavras originais
def obter_indices(palavra, palavra_unica):
    indices = [palavra_unica.index(letra) for letra in palavra if letra in palavra_unica]
    return indices

# Função para converter uma lista de índices em um número decimal
def indices_para_decimal(indices):
    numero_str = ''.join(map(str, indices))
    return int(numero_str) if numero_str else 0

# Função para mutação
def mutacao(vetor, taxa_mutacao):
    for _ in range(int(len(vetor) * taxa_mutacao)):
        idx1, idx2 = np.random.choice(len(vetor), 2, replace=False)
        vetor[idx1], vetor[idx2] = vetor[idx2], vetor[idx1]
    return vetor

# Função para crossover ciclico
def crossover_ciclico(pai1, pai2):
    filho1, filho2 = np.copy(pai1), np.copy(pai2)
    start = np.random.randint(len(pai1))
    pos = start
    while True:
        filho1[pos], filho2[pos] = filho2[pos], filho1[pos]
        pos = np.where(pai1 == pai2[pos])[0][0]
        if pos == start:
            break
    return filho1, filho2

# Função para crossover PMX
def crossover_pmx(pai1, pai2):
    size = len(pai1)
    p1, p2 = np.zeros(size, dtype=int), np.zeros(size, dtype=int)
    
    cxpoint1, cxpoint2 = sorted(np.random.choice(size, 2, replace=False))
    
    for i in range(cxpoint1, cxpoint2):
        p1[pai1[i]] = pai2[i]
        p2[pai2[i]] = pai1[i]

    for i in range(size):
        if not p1[pai1[i]]:
            p1[pai1[i]] = pai1[i]
        if not p2[pai2[i]]:
            p2[pai2[i]] = pai2[i]

    return p1, p2

# Função para executar a troca simples
def trocar_simples(vetor):
    idx1, idx2 = np.random.choice(len(vetor), 2, replace=False)
    vetor[idx1], vetor[idx2] = vetor[idx2], vetor[idx1]
    return vetor

# Função para avaliar individuo
def avaliar_individuo(individuo, indices_palavra_unica, indices_palavras):
    return indices_para_decimal(individuo) - (
        indices_para_decimal(indices_palavras[0]) + indices_para_decimal(indices_palavras[1])
    )

# Função para executar o algoritmo genético
def executar_ag(palavra_unica, indices_palavra_unica, indices_palavras, metodo_mutacao, taxa_mutacao, metodo_crossover, taxa_crossover, metodo_reinsercao, geracoes=50):
    populacao = [np.random.permutation(indices_palavra_unica) for _ in range(100)]
    # Para salvar os vetores originais e mutados
    originais = []
    mutados = []
    cruzamentos = []

    for geracao in range(geracoes):
        nova_populacao = []

        # Crossover
        for _ in range(int(100 * taxa_crossover) // 2):
            pai1, pai2 = random.sample(populacao, 2)
            if metodo_crossover == "ciclico":
                filho1, filho2 = crossover_ciclico(pai1, pai2)
            elif metodo_crossover == "pmx":
                filho1, filho2 = crossover_pmx(pai1, pai2)
            nova_populacao.extend([filho1, filho2])
            cruzamentos.append((pai1, pai2, filho1, filho2))

        # Mutação
        nova_populacao_mutada = []
        for individuo in nova_populacao:
            if metodo_mutacao == "troca":
                individuo_mutado = trocar_simples(np.copy(individuo))
            else:
                individuo_mutado = mutacao(np.copy(individuo), taxa_mutacao)
            nova_populacao_mutada.append(individuo_mutado)
            originais.append(individuo)
            mutados.append(individuo_mutado)

        # Reinserção
        if metodo_reinsercao == "ordenada":
            populacao.extend(nova_populacao_mutada)
            populacao = sorted(populacao, key=lambda ind: avaliar_individuo(ind, indices_palavra_unica, indices_palavras))[:100]
        elif metodo_reinsercao == "elitismo":
            elite = sorted(populacao, key=lambda ind: avaliar_individuo(ind, indices_palavra_unica, indices_palavras))[:20]
            populacao = random.sample(populacao, 80) + nova_populacao_mutada
            populacao = elite + random.sample(populacao, 80)
    
    melhor_individuo = min(populacao, key=lambda ind: avaliar_individuo(ind, indices_palavra_unica, indices_palavras))
    fitness = avaliar_individuo(melhor_individuo, indices_palavra_unica, indices_palavras)
    return melhor_individuo, fitness, originais, mutados, cruzamentos

# Função para processar as palavras e gerar os vetores
def processar_palavras():
    palavras = [entry1.get(), entry2.get(), entry3.get()]
    palavra_unica = letras_unicas(palavras)

    # Verifica se a palavra gerada ultrapassa 10 caracteres
    if len(palavra_unica) > 10:
        messagebox.showerror("Erro", "O resultado da palavra formada excede 10 caracteres.")
    else:
        indices_palavras = [obter_indices(palavra, palavra_unica) for palavra in palavras]
        indices_palavra_unica = list(range(len(palavra_unica)))

        # Calcula números decimais para cada palavra
        numeros_decimais = [indices_para_decimal(indices) for indices in indices_palavras]
        numero_decimal_palavra_unica = indices_para_decimal(indices_palavra_unica)

        # Subtração da soma dos números decimais da primeira e segunda palavra da terceira
        subtracao = numeros_decimais[2] - (numeros_decimais[0] + numeros_decimais[1])

        # Geração dos 100 vetores
        vetores = []
        for _ in range(100):
            indices_palavras_aleatorios = [
                np.random.permutation(indices_palavras[0]),
                np.random.permutation(indices_palavras[1]),
                np.random.permutation(indices_palavras[2])
            ]
            subtracao_aleatoria = indices_para_decimal(indices_palavras_aleatorios[2]) - (
                indices_para_decimal(indices_palavras_aleatorios[0]) + indices_para_decimal(indices_palavras_aleatorios[1])
            )
            # Inclui a palavra_unica no vetor
            vetor_com_palavra_unica = np.concatenate([indices_palavra_unica, indices_palavras_aleatorios[1]])
            vetor_com_palavra_unica = np.unique(vetor_com_palavra_unica)  # Remove duplicatas
            np.random.shuffle(vetor_com_palavra_unica)  # Embaralha o vetor
            vetores.append((vetor_com_palavra_unica, subtracao_aleatoria))

        # Exibir o resultado
        resultado = f"Palavra Formada: {palavra_unica}\n"
        
        # Adiciona a posição de cada letra na palavra formada
        posicoes_letras = [f"{letra}: {i}" for i, letra in enumerate(palavra_unica)]
        resultado += "Posição das Letras na Palavra Formada:\n" + "\n".join(posicoes_letras) + "\n"
        
        for i, (palavra, indices) in enumerate(zip(palavras, indices_palavras)):
            resultado += f"\nPalavra {i + 1}: {palavra}\nÍndices: {indices}\nNúmero Decimal: {indices_para_decimal(indices)}"
        resultado += f"\n\nfitness: = {subtracao}"
        resultado_label.config(text=resultado)

# Função para gerar o arquivo de resultados
def gerar_arquivo_resultados():
    palavras = [entry1.get(), entry2.get(), entry3.get()]
    palavra_unica = letras_unicas(palavras)
    indices_palavras = [obter_indices(palavra, palavra_unica) for palavra in palavras]
    indices_palavra_unica = list(range(len(palavra_unica)))

    metodos_mutacao = ["troca", "random"]
    taxas_mutacao = [0.05, 0.10]
    metodos_crossover = ["ciclico", "pmx"]
    taxas_crossover = [0.60, 0.80]
    metodos_reinsercao = ["ordenada", "elitismo"]

    resultados = []
    
    with open("resultados.txt", "w") as arquivo:
        for metodo_mutacao in metodos_mutacao:
            for taxa_mutacao in taxas_mutacao:
                for metodo_crossover in metodos_crossover:
                    for taxa_crossover in taxas_crossover:
                        for metodo_reinsercao in metodos_reinsercao:
                            if metodo_reinsercao == "elitismo" and taxa_crossover != 0.80:
                                continue
                            inicio = time.time()
                            fitnesses = []
                            originais = []
                            mutados = []
                            cruzamentos = []
                            for _ in range(1000):
                                _, fitness, originais, mutados, cruzamentos = executar_ag(palavra_unica, indices_palavra_unica, indices_palavras, metodo_mutacao, taxa_mutacao, metodo_crossover, taxa_crossover, metodo_reinsercao)
                                fitnesses.append(fitness)
                            fim = time.time()
                            tempo_execucao = fim - inicio
                            convergencia = len([f for f in fitnesses if f == 0]) / 1000
                            resultados.append((metodo_mutacao, taxa_mutacao, metodo_crossover, taxa_crossover, metodo_reinsercao, convergencia, tempo_execucao))
                            # Salvando informações dos vetores
                            arquivo.write(f"\nMétodo Mutação: {metodo_mutacao}, Taxa Mutação: {taxa_mutacao}, Método Crossover: {metodo_crossover}, Taxa Crossover: {taxa_crossover}, Método Reinserção: {metodo_reinsercao}\n")
                            arquivo.write("Originais e Mutados:\n")
                            for original, mutado in zip(originais, mutados):
                                arquivo.write(f"Original: {original}, Mutado: {mutado}\n")
                            arquivo.write("Cruzamentos (Pais e Filhos):\n")
                            for pai1, pai2, filho1, filho2 in cruzamentos:
                                arquivo.write(f"Pai1: {pai1}, Pai2: {pai2}, Filho1: {filho1}, Filho2: {filho2}\n")
                            # Adiciona detalhes do algoritmo de troca
                            if metodo_mutacao == "troca":
                                arquivo.write("Algoritmo de Troca Simples:\n")
                                for original, mutado in zip(originais, mutados):
                                    arquivo.write(f"Original: {original}, Mutado: {mutado}\n")
    
    messagebox.showinfo("Concluído", "Os resultados foram gerados e salvos em 'resultados.txt'.")

# Configuração da GUI
root = tk.Tk()
root.title("Processador de Palavras")

tk.Label(root, text="Digite a primeira palavra:").grid(row=0, column=0)
entry1 = tk.Entry(root)
entry1.grid(row=0, column=1)

tk.Label(root, text="Digite a segunda palavra:").grid(row=1, column=0)
entry2 = tk.Entry(root)
entry2.grid(row=1, column=1)

tk.Label(root, text="Digite a terceira palavra:").grid(row=2, column=0)
entry3 = tk.Entry(root)
entry3.grid(row=2, column=1)

tk.Button(root, text="Processar", command=processar_palavras).grid(row=3, columnspan=2)

resultado_label = tk.Label(root, text="")
resultado_label.grid(row=4, columnspan=2)

tk.Button(root, text="Gerar Resultados", command=gerar_arquivo_resultados).grid(row=5, columnspan=2)

root.mainloop()
