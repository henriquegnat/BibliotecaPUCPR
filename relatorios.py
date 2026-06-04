import datetime
import math

import dados
from livros import buscar_livro_por_id
from usuarios import buscar_usuario_por_id
from relatorios import cabecalho, linha


def mostrar_relatorio():  # AQUI ELE EXIBE O RELATÓRIO RESUMIDO
    cabecalho("RELATORIO DA BIBLIOTECA")
    print(" (1) Resumo Geral (2) Detalhar empréstimos ativos")
    tipo = input(" Tipo de relatório: ").strip()

    if tipo == "2":
        from emprestimos import listar_emprestimos  
        listar_emprestimos()
        return

    total_livros = len(dados.livros)
    total_usuarios = len(dados.usuarios)
    total_ativos = len(dados.emprestimos)   
    total_historico = len(dados.historico)
    total_multas = sum(u["multa_acumulada"] for u in dados.usuarios)

    print(f" Livros no acervo: {total_livros}")
    print(f" Usuários cadastrados: {total_usuarios}")
    print(f" Empréstimos ativos: {total_ativos}")
    print(f" Devoluções realizadas: {total_historico}")
    print(f" Multas a receber:      R$ {total_multas:.2f}")

    if total_historico > 0: 
        atrasados = sum(1 for h in dados.historico if h["multa"] > 0)
        pct = math.floor((atrasados / total_historico) * 100)
        print(f" Devoluções com atraso: {atrasados} ({pct}%)") 


def salvar_relatorio():  # AQUI ELE SALVA O RELATÓRIO EM UM ARQUIVO (.TXT)
    nome_arquivo = f"relatorio_biblioteca_{datetime.date.today()}.txt"
    with open(nome_arquivo, "w", encoding="utf-8") as f:  
        f.write("=" * 55 + "\n")
        f.write(" RELATÓRIO FINAL - SISTEMA DE BIBLIOTECA \n")
        f.write(f" Gerado em: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")  
        f.write("=" * 55 + "\n\n")

        f.write("── LIVROS DO ACERVO ──\n")
        for livro in dados.livros:  
            f.write(f"[{livro['id']}] {livro['titulo']} - {livro['autor']} ({livro['ano']})\n") 
            f.write(f"     Disponíveis: {livro['quantidade_disponivel']}/{livro['quantidade_total']}\n")  

        f.write("\n── USUÁRIOS ──\n")
        for usuario in dados.usuarios:  
            f.write(f"[{usuario['id']}] {usuario['nome']} | Multa: R$ {usuario['multa_acumulada']:.2f}\n")

        f.write("\n── EMPRÉSTIMOS ATIVOS ──\n")
        for emp in dados.emprestimos: 
            u = buscar_usuario_por_id(emp["usuario_id"])
            l = buscar_livro_por_id(emp["livro_id"])
            f.write(f"  {l['titulo']} → {u['nome']} | Devolução: {emp['data_prevista']}\n")

        f.write("\n── HISTÓRICO DE DEVOLUÇÕES ──\n")
        for h in dados.historico:
            u = buscar_usuario_por_id(h["usuario_id"])
            l = buscar_livro_por_id(h["livro_id"])
            f.write(f"  {l['titulo']} → {u['nome']} | Multa: R$ {h['multa']:.2f}\n")

        f.write("\n" + "=" * 55 + "\n")
        f.write("  Fim do relatório.\n")

    print(f"\n  ✔ Relatório salvo em '{nome_arquivo}'.")
    return nome_arquivo