import os

def linha (char="-", largura=55):
    print(char * largura)

def cabecalho(titulo):
    linha("=")
    print(f"{titulo}")
    linha("=")

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

def pausar():
    input("\n Pressione ENTER para continuar...")