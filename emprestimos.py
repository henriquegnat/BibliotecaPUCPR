# Funções de empréstimos e devoluções 

import datetime
import math

import dados 
from constantes import LIMITE_EMPRESTIMOS, PRAZO_DEVOLUCAO, MULTA_POR_DIA, MULTA_MAXIMA
from auxiliares import cabecalho, linha

# *** Funções de empréstimos e multa ***

def contar_emprestimos_usuario(usuario_id): # Essa função consegue contar quantos empréstimos um usuário tem atualmente.
    return sum(1 for emprestimo in dados.emprestimos if emprestimo[usuario_id] == usuario_id)

def emprestimo_ativo(livro_id): # Essa função verifica se um livro específico já está emprestado
    for emp in dados.emprestimos:
        if emp["livro_id"] == livro_id:
            return emp
    return None

def calcular_multa(data_prevista_str): # Essa função calcula a multa com base na data prevista de devolução e a data atual.
    data_prevista = datetime.datetime.strptime(data_prevista_str, "%Y-%m-%d").date()
    hoje = datetime.date.today()
    atraso = (hoje - data_prevista).days
    if atraso <=0: 
        return 0.0
    
    multa = atraso * MULTA_POR_DIA
    multa = min(multa, MULTA_MAXIMA)
    return round(multa, 2)

# *** Funções principais ***

def realizar_emprestimo():
    from livros import buscar_livro_por_id
    from usuarios import buscar_usuario_por_id
    
    cabecalho("Realizar Empréstimo")
    uid = input("Digite o ID do usuário: ")
    lid = input("Digite o ID do livro: ")

    if not uid.isdigit() or not lid.isdigit():
        print("IDs inválidos. Por favor, insira números.")
        return
    
    usuario = buscar_usuario_por_id(int(uid))
    livro = buscar_livro_por_id(int(lid))

    # Condicionais 

    if not usuario:
        print("Usuário não encontrado.")
        return
    
    if not livro:
        print("Livro não encontrado.")
        return
    
    if livro ["quantidade_disponível"] <= 0:
        print(f"O Livro '{livro['titulo']}' não está disponível para empréstimo no momento.")
        return
    
    if contar_emprestimos_usuario(usuario["id"]) >= LIMITE_EMPRESTIMOS:
        print(f"O usuário '{usuario['nome']}' já atingiu o limite de {LIMITE_EMPRESTIMOS} empréstimos.")
        return
    
    if usuario["multa_acumulada"] > 0:
        print(f"O usuário '{usuario['nome']}' possui uma multa de R${usuario['multa_acumulada']:.2f}.")
        return
    
    hoje = datetime.date.today()
    data_prevista = hoje + datetime.timedelta(days=PRAZO_DEVOLUCAO)

    emprestimo = {
        "id":               len(dados.emprestimos) + len(dados.historico) + 1,
        "usuario_id":       usuario["id"],
        "livro_id":         livro["id"],
        "data_emprestimo":  str(hoje),
        "data_prevista":    str(data_prevista),
    }
    dados.emprestimos.append(emprestimo)
    livro["quantidade_disponivel"] -= 1    

    print(f"\nEmpréstimo realizado!")
    print(f"Livro: {livro['titulo']}")
    print(f"Usuário: {usuario['nome']}")
    print(f"Devolução prevista: {data_prevista.strftime('%d/%m/%Y')}")


def devolver_livro(): # Essa função é responsável por processar a devolução de um livro, calcular multas se houver atraso e atualizar os registros de empréstimos e histórico.
    from livros import buscar_livro_por_id 
    from usuarios import buscar_usuario_por_id

    cabecalho("DEVOLVER LIVRO")
    lid = input("ID do livro a devolver: ").strip()

    if not lid.isdigit():
        print("ID inválido.")
        return

    emprestimo = emprestimo_ativo(int(lid))
    if not emprestimo:
        print("Nenhum empréstimo ativo encontrado para esse livro.")
        return

    usuario = buscar_usuario_por_id(emprestimo["usuario_id"])
    livro = buscar_livro_por_id(emprestimo["livro_id"])
    multa = calcular_multa(emprestimo["data_prevista"])

    livro["quantidade_disponivel"] += 1    # devolve exemplar ao acervo
    dados.emprestimos.remove(emprestimo)

    emprestimo["data_devolucao_real"] = str(datetime.date.today())
    emprestimo["multa"] = multa
    dados.historico.append(emprestimo)

    if multa > 0:
        usuario["multa_acumulada"] += multa
        print(f"\nDevolução com atraso! Multa de R$ {multa:.2f} gerada.")
    else:
        print(f"\n'{livro['titulo']}' devolvido no prazo. Sem multa.")

    print(f"Usuário: {usuario['nome']}")


def listar_emprestimos():
    """Lista todos os empréstimos ativos com status de prazo."""
    from livros import buscar_livro_por_id
    from usuarios import buscar_usuario_por_id

    cabecalho("EMPRÉSTIMOS ATIVOS")
    if not dados.emprestimos:
        print("Nenhum empréstimo ativo.")
        return

    hoje = datetime.date.today()
    for emp in dados.emprestimos:
        usuario = buscar_usuario_por_id(emp["usuario_id"])
        livro = buscar_livro_por_id(emp["livro_id"])
        prevista = datetime.datetime.strptime(emp["data_prevista"], "%Y-%m-%d").date()
        atraso = (hoje - prevista).days
        status = f"{atraso} dia(s) de atraso" if atraso > 0 else "No prazo"

        print(f"Livro: {livro['titulo']}")
        print(f"Usuário: {usuario['nome']}")
        print(f"Emprestado: {emp['data_emprestimo']} | Previsto: {emp['data_prevista']} | {status}")
        linha("-", 55)

