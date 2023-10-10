import sys
import requests
import json
import tkinter as tk
from tkinter import messagebox
import threading
import time
import datetime



# Variável global para armazenar o valor atual
janela_aberta = True
valor_atual = "Trava Invalida"
valores_anteriores = []
thread_ativa = True

# Dicionário para associar os meses às letras referente ao calendario Dólar Futuro
meses_letras = {
    "JAN 2023 6LF3": "F",
    "FEV 2023 6LG3": "G",
    "MAR 2023 6LH3": "H",
    "ABR 2023 6LJ3": "J",
    "MAI 2023 6LK3": "K",
    "JUN 2023 6LM3": "M",
    "JUL 2023 6LN3": "N",
    "AGO 2023 6LQ3": "Q",
    "SET 2023 6LU3": "U",
    "OUT 2023 6LV3": "V",
    "NOV 2023 6LX3": "X",
    "DEZ 2023 6LZ3": "Z"
}


# Função para fechar a janela quando o botão "Confirmar" é clicado
def confirmar_selecao():
    
    root.destroy()

def atualizar_opcoes():
    hoje = datetime.date.today()
    mes_atual = hoje.strftime("%B")

    # Encontre a letra associada ao mês atual
    letra_mes_atual = meses_letras.get(mes_atual)

    if letra_mes_atual is None:
        # Mês atual não encontrado no dicionário, use 'F' como padrão
        letra_mes_atual = "F"

    opcoes = []

    # Encontre o índice da letra do mês atual nas letras ordenadas
    indice_letra_atual = list(meses_letras.values()).index(letra_mes_atual)

    for i in range(12):
        indice = (indice_letra_atual + i) % 12
        mes = list(meses_letras.keys())[indice]
        letra = list(meses_letras.values())[indice]
        opcoes.append(f"{letra}     \t{mes}")

    opcao_selecionada.set(opcoes[0])  # Defina o primeiro mês como padrão
    caixa_selecao['menu'].delete(0, 'end')  # Limpe todas as opções atuais

    for mes in opcoes:
        caixa_selecao['menu'].add_command(label=mes, command=tk._setit(opcao_selecionada, mes))

# Criar a janela principal
root = tk.Tk()
root.title("Trava CME")
root.attributes('-toolwindow', 1)
root.resizable(False, False)



# Obter a largura e a altura da tela
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()


# Definir o tamanho desejado da janela
window_width = 300
window_height = 150


# Calcular a posição para centralizar a janela
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Configurar a geometria da janela para centralizá-la
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Variável para armazenar a letra selecionada
letra_selecionada = None

label_instrucoes = tk.Label(root, text="Selecione o mês para consultar a Trava:")
label_instrucoes.pack(padx=10, pady=5)

# Caixa de seleção
opcao_selecionada = tk.StringVar(root)
caixa_selecao = tk.OptionMenu(root, opcao_selecionada, "")
caixa_selecao.pack(padx=10, pady=5)

# Botão para confirmar a seleção
botao_confirmar = tk.Button(root, text="Confirmar", command=confirmar_selecao)
botao_confirmar.pack(padx=10, pady=10)

# Atualizar as opções da caixa de seleção
atualizar_opcoes()

# Iniciar a interface gráfica
root.mainloop()

# Após o usuário selecionar um mês, a variável 'letra_selecionada' terá o valor correspondente
letra_selecionada = opcao_selecionada.get().split()[0]
print(f"Letra selecionada: {letra_selecionada}")


def fechar_janela():
    global janela_aberta
    janela_aberta = False
    root.destroy()


def fechar_programa():
    global thread_ativa
    thread_ativa = False
    fechar_janela()
    sys.exit(0)

# Função para buscar o valor atual
def buscar_valor_atual():
    try:
        global valor_atual, valores_anteriores
        print(valor_atual)
        # URL do JSON
        url = f"https://www.cmegroup.com/CmeWS/mvc/Quotes/Option/41/G/{letra_selecionada}3/ATM?optionProductId=41&strikeRange=ATM&isProtected&_t=1695840342774"

        # Fazer a solicitação GET para a URL
        response = requests.get(url)

        # Verificar se a solicitação foi bem-sucedida
        if response.status_code == 200:
            # Converter o conteúdo da resposta para um objeto JSON
            data = response.json()

            # Inicializar a lista de valores de strike rank igual a 1
            strike_ranks = []

            # Iterar sobre a lista de contratos de opção
            for contract in data["optionContractQuotes"]:
                if contract["strikeRank"] == 1:
                    strike_ranks.append(contract["strikePrice"])

            # Verificar se pelo menos um valor de strike rank igual a 1 foi encontrado
            if strike_ranks:
                # Calcular 1 dividido pelo cada valor de strike rank igual a 1 e arredondar
                novos_valores = [round(1 / float(strike), 4) for strike in strike_ranks]

                # Verificar se os novos valores são diferentes dos valores anteriores
                if novos_valores != valores_anteriores:
                    # Emitir um alerta com os novos valores
                    mensagem = f"Trava CME:\n"
                    for i, novo_valor in enumerate(novos_valores, start=1):
                        mensagem += f"Trava {i}: {novo_valor}\n"
                    valor_atual = novos_valores
                    
                    messagebox.showinfo("Alerta", mensagem)

                # Atualizar os valores anteriores
                valores_anteriores = novos_valores

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")
        fechar_programa()


# Função para buscar o valor atual periodicamente
def buscar_valor_periodicamente():
    while thread_ativa:
        buscar_valor_atual()
        time.sleep(30)   # Aguardar 30 segundos antes da próxima verificação

# Criar uma thread para buscar o valor periodicamente
busca_thread = threading.Thread(target=buscar_valor_periodicamente)

# Criar a janela principal
root = tk.Tk()
root.title("CME Trava")
root.resizable(False, False)
root.protocol("WM_DELETE_WINDOW",fechar_programa)


# Calculate the center coordinates
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 350  # Set your desired window width
window_height = 100  # Set your desired window height
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

# Set the window size and position
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Rótulo para exibir o valor atual
label_valor_atual = tk.Label(root, text="Valor Atual da Trava CME: ", font=("Helvetica", 12))
label_valor_atual.pack(pady=10)

# Botão para fechar o programa
botao_fechar = tk.Button(root, text="Fechar", command=fechar_programa)
botao_fechar.pack(padx=50, pady=10)


# Iniciar a thread de busca
busca_thread.start()

# Função para atualizar o rótulo com o valor atual
def atualizar_label_valor():
    global valor_atual, janela_aberta

    # Verificar se a janela ainda está aberta
    if janela_aberta:
        label_valor_atual.config(text=f"Valor Atual da Trava CME: R$ {valor_atual}")
        


# Timer para atualizar o rótulo a cada segundo
def atualizar_timer():
    if janela_aberta:
        atualizar_label_valor()
        root.after(1000, atualizar_timer)  # Agenda a função para ser chamada novamente após 1 segundo (1000 ms)


def root_destruir():
    global thread_ativa
    thread_ativa = False  # Define a variável de controle para False para encerrar a thread
    root.destroy()
    sys.exit(0)        

# Criar uma thread para atualizar o rótulo com o valor atual
atualizacao_thread = threading.Thread(target=atualizar_timer)
atualizacao_thread.daemon = True  # Define a thread como daemon para que ela seja encerrada quando a janela for fechada

# Iniciar a thread de atualização do rótulo
atualizacao_thread.start()

# Iniciar a interface gráfica
root.mainloop()
