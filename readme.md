# 📚 Sistema de Biblioteca — PUCPR

Sistema de gerenciamento de biblioteca em Python, desenvolvido para controlar o acervo de livros, cadastro de usuários, empréstimos e devoluções.

## Como rodar

Certifique-se de ter o Python instalado, depois execute:

```bash
python main.py
```

## Funcionalidades

- Cadastrar, listar e pesquisar livros do acervo
- Cadastrar e listar usuários
- Realizar empréstimos e devoluções
- Controle automático de multas por atraso
- Geração de relatório ao encerrar o sistema

## Regras do sistema

- Limite de 3 livros emprestados por usuário
- Prazo de devolução: 14 dias
- Multa por atraso: R$ 2,50 por dia
- Teto de multa: R$ 50,00

## Estrutura dos arquivos

| Arquivo | Descrição |
|---|---|
| `main.py` | Arquivo principal — roda os menus e junta todos os módulos |
| `livros.py` | Cadastro, listagem e pesquisa de livros |
| `usuarios.py` | Cadastro, listagem de usuários e pagamento de multas |
| `emprestimos.py` | Realização de empréstimos, devoluções e listagem |
| `relatorios.py` | Geração e exibição de relatórios |
| `dados.py` | Listas que guardam o estado do sistema em memória |
| `constantes.py` | Configurações do sistema (limites, prazos, valores de multa) |
| `auxiliares.py` | Funções utilitárias usadas em todo o sistema |

## Observações

- Os dados ficam em memória enquanto o sistema está rodando. Ao encerrar, um relatório é salvo automaticamente.
- O sistema foi desenvolvido e testado com Python 3.