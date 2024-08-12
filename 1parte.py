import numpy as np 
# Importa a biblioteca numpy para manipulacao de arrays e operacoes matematicas
import tkinter as tk 
# Importa a biblioteca tkinter para criacao de interfaces graficas
from tkinter import messagebox  
# Importa a funcionalidade de messagebox do tkinter para exibir mensagens

# Funcao para obter letras unicas de tres palavras
def letras_unicas(palavras):
    todas_letras = ''.join(palavras)  
    # Junta todas as palavras em uma string unica
    letras_unicas = ''.join(sorted(set(todas_letras), key=todas_letras.index)) 
    # Remove letras duplicadas, mantendo a ordem original
    return letras_unicas  
# Retorna a string com letras unicas

# Funcao para obter os indices das letras nas palavras originais
def obter_indices(palavra, palavra_unica):
    #(in lista objeto que seja iteravel)
    indices = [palavra_unica.index(letra) for letra in palavra if letra in palavra_unica]  
    # Para cada letra na palavra, obtém o indice dela na palavra unica
    return indices  
# Retorna a lista de indices

# Funcao para converter uma lista de indices em um numero decimal
def indices_para_decimal(indices):
    #map: Esta funcao aplica uma funcao a cada item de uma sequencia
    #str: Esta e a funcao que converte um valor para uma string
    #indices: E a lista de valores que sera processada
    numero_str = ''.join(map(str, indices))  
    # Converte cada indice para string e junta todos em uma unica string
    return int(numero_str) if numero_str else 0  
#numero_str = ''.join(map(str, indices)) :Esta parte converte a variável numero_str de uma string para um número inteiro.
# Converte a string resultante em um numero inteiro, ou retorna 0 se a string estiver vazia

# Funcao para processar as palavras e gerar os vetores
def processar_palavras():
    #Entry, que representa um campo de entrada de texto na interface gráfica criada com Tkinter
    #get, que retorna o texto atualmente inserido no campo de entrada
    palavras = [entry1.get(), entry2.get(), entry3.get()] 
    # Obtem as palavras digitadas pelo usuario nos campos de entrada
    palavra_unica = letras_unicas(palavras)  
    # Gera uma palavra com as letras unicas das palavras fornecidas

    # Verifica se a palavra gerada ultrapassa 10 caracteres
    if len(palavra_unica) > 10:
        messagebox.showerror("Erro", "O resultado da palavra formada excede 10 caracteres.") 
        # Exibe uma mensagem de erro se a palavra tiver mais de 10 letras
    else:
        indices_palavras = [obter_indices(palavra, palavra_unica) for palavra in palavras]  
        # Obtem os indices das letras de cada palavra na palavra unica
        indices_palavra_unica = list(range(len(palavra_unica)))  
        # Gera uma lista de indices para a palavra unica

        # Calcula numeros decimais para cada palavra
        numeros_decimais = [indices_para_decimal(indices) for indices in indices_palavras]  
        # Converte os indices das palavras em numeros decimais
        numero_decimal_palavra_unica = indices_para_decimal(indices_palavra_unica) 
        # Converte os indices da palavra unica em um numero decimal

        # Subtracao da soma dos numeros decimais da primeira e segunda palavra da terceira
        subtracao = numeros_decimais[2] - (numeros_decimais[0] + numeros_decimais[1])  
        # Calcula a subtracao conforme descrita

        # Geracao dos 100 vetores
        vetores = []
        for _ in range(100):  # Loop para gerar 100 vetores
            indices_palavras_aleatorios = [
                np.random.permutation(indices_palavras[0]),  
                # Embaralha os indices da primeira palavra
                np.random.permutation(indices_palavras[1]),  
                # Embaralha os indices da segunda palavra
                np.random.permutation(indices_palavras[2]) 
                # Embaralha os indices da terceira palavra
            ]
            subtracao_aleatoria = indices_para_decimal(indices_palavras_aleatorios[2]) - (
                indices_para_decimal(indices_palavras_aleatorios[0]) + indices_para_decimal(indices_palavras_aleatorios[1])
            )  # Calcula a subtracao dos numeros decimais embaralhados

            # Inclui a palavra_unica no vetor
            #np é uma convenção comum para importar a biblioteca NumPy em Python
            vetor_com_palavra_unica = np.concatenate([indices_palavra_unica, indices_palavras_aleatorios[1]])  
            # Concatena os indices da palavra unica com os indices embaralhados
            vetor_com_palavra_unica = np.unique(vetor_com_palavra_unica)  
            # Remove duplicatas do vetor
            np.random.shuffle(vetor_com_palavra_unica)  
            # Embaralha o vetor resultante

            # Realiza a mutacao (troca de duas posicoes)
            vetor_mutado = vetor_com_palavra_unica.copy()  
            # Cria uma copia do vetor original
            pos1, pos2 = np.random.choice(len(vetor_mutado), 2, replace=False)  
            # Seleciona aleatoriamente duas posicoes diferentes no vetor
            vetor_mutado[pos1], vetor_mutado[pos2] = vetor_mutado[pos2], vetor_mutado[pos1]  
            # Troca os elementos nas posicoes selecionadas

            vetores.append((vetor_com_palavra_unica, vetor_mutado, subtracao_aleatoria))  
            # Adiciona o vetor original, mutado e a subtracao a lista de vetores

        # Exibir o resultado
        resultado = f"Palavra Formada: {palavra_unica}\n"  # Prepara a string de resultado
        
        # Adiciona a posicao de cada letra na palavra formada
        posicoes_letras = [f"{letra}: {i}" for i, letra in enumerate(palavra_unica)]  
        # Gera a lista de letras com suas respectivas posicoes
        resultado += "Posicao das Letras na Palavra Formada:\n" + "\n".join(posicoes_letras) + "\n"  
        # Adiciona as posicoes das letras ao resultado
        
        for i, (palavra, indices) in enumerate(zip(palavras, indices_palavras)):  
            # Itera sobre as palavras e seus indices
            resultado += f"\nPalavra {i + 1}: {palavra}\nIndices: {indices}\nNumero Decimal: {indices_para_decimal(indices)}"  
            # Adiciona as informacoes de cada palavra ao resultado
        
        resultado += f"\n\nfitness: = {subtracao}"  
        # Adiciona o valor do fitness ao resultado

        # Adiciona os 100 vetores
        for i, (vetor, vetor_mutado, subtracao_aleatoria) in enumerate(vetores[:100]):  
            # Mostra apenas os primeiros 100 vetores
            print("Vetor", i + 1)  
            # Imprime o numero do vetor
            
            # Imprime os vetores aleatorios para cada palavra
            print("Palavra 1 (Aleatoria):", indices_palavras_aleatorios[0])  
            # Imprime o vetor aleatorio da palavra 1
            print("Palavra 2 (Aleatoria):", indices_palavras_aleatorios[1])  
            # Imprime o vetor aleatorio da palavra 2
            print("Palavra 3 (Aleatoria):", indices_palavras_aleatorios[2])  
            # Imprime o vetor aleatorio da palavra 3
            
            # Imprime o vetor original e o vetor mutado
            print("~~~Original~~", vetor)  
            # Imprime o vetor original
            print("Vetor Mutado:", vetor_mutado)  
            # Imprime o vetor mutado
            print("fitness:", subtracao_aleatoria)  
            # Imprime o valor do fitness para o vetor aleatorio

        resultado_label.config(text=resultado)  
        # Atualiza o texto do label de resultado com as informacoes processadas

# Configuracao da GUI
root = tk.Tk()  # Cria a janela principal da aplicacao
root.title("algoritmo genetico criptoaritmetica")  
# Define o titulo da janela

tk.Label(root, text="Digite a primeira palavra:").grid(row=0, column=0)  
# Cria um label para a primeira palavra
entry1 = tk.Entry(root)  
# Cria um campo de entrada para a primeira palavra
entry1.grid(row=0, column=1)  
# Posiciona o campo de entrada na interface

tk.Label(root, text="Digite a segunda palavra:").grid(row=1, column=0)  
# Cria um label para a segunda palavra
entry2 = tk.Entry(root)  
# Cria um campo de entrada para a segunda palavra
entry2.grid(row=1, column=1)  
# Posiciona o campo de entrada na interface

tk.Label(root, text="Digite a terceira palavra:").grid(row=2, column=0)  
# Cria um label para a terceira palavra
entry3 = tk.Entry(root)  
# Cria um campo de entrada para a terceira palavra
entry3.grid(row=2, column=1)  
# Posiciona o campo de entrada na interface

tk.Button(root, text="Processar", command=processar_palavras).grid(row=3, columnspan=2)  
# Cria um botao que chama a funcao processar_palavras ao ser clicado

resultado_label = tk.Label(root, text="")  
# Cria um label vazio para mostrar o resultado
resultado_label.grid(row=4, columnspan=2)  
# Posiciona o label de resultado na interface

root.mainloop()  
# Inicia o loop principal da interface grafica
