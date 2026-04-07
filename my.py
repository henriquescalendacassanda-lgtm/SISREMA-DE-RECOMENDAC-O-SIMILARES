# SISREMA-DE-RECOMENDAC-O-SIMILARES
Este é um código completo para o desenvolvimento de um Sistema de Secomndações Similares

from math import sqrt

usuarios = {
    "Ana": {"Arroz": 5, "Leite": 3, "Açúcar": 4},
    "Bruno": {"Arroz": 3, "Leite": 4, "Óleo": 5},
    "Carlos": {"Arroz": 4, "Açúcar": 2, "Leite": 5},
    "Diana": {"Óleo": 4, "Açúcar": 3, "Leite": 2},
    "Eduardo": {"Arroz": 2, "Leite": 5, "Óleo": 3}
}

def similaridade_euclidiana(u1, u2):
    comum = [item for item in usuarios[u1] if item in usuarios[u2]]
    if not comum:
        return 0
    soma = sum((usuarios[u1][i] - usuarios[u2][i])**2 for i in comum)
    return 1 / (1 + sqrt(soma))

def recomendar(usuario):
    totais = {}
    soma_sim = {}
    for outro in usuarios:
        if outro == usuario:
            continue
        sim = similaridade_euclidiana(usuario, outro)
        if sim <= 0:
            continue
        for item in usuarios[outro]:
            if item not in usuarios[usuario]:
                totais[item] = totais.get(item, 0) + usuarios[outro][item] * sim
                soma_sim[item] = soma_sim.get(item, 0) + sim
    if not totais:
        return []
    rankings = [(item, round(totais[item] / soma_sim[item], 2)) for item in totais]
    rankings.sort(key=lambda x: x[1], reverse=True)
    return rankings[:3]

def adicionar():
    nome = input("Nome do usuário: ").strip()
    if nome not in usuarios:
        usuarios[nome] = {}
        print(f"Novo usuário '{nome}' criado.")
    produto = input("Produto: ").strip()
    nota = input("Nota: ").strip()
    try:
        nota = float(nota)
        usuarios[nome][produto] = nota
        print(f"{produto} adicionado para {nome} com nota {nota}.")
    except ValueError:
        print("Nota inválida.")

def tabela_usuarios():
    if not usuarios:
        print("Nenhum usuário adicionado.")
        return
    todos_produtos = set()
    for produtos in usuarios.values():
        todos_produtos.update(produtos.keys())
    todos_produtos = sorted(todos_produtos)
    col_user_width = max(len("Usuário"), max(len(u) for u in usuarios))
    col_prod_widths = {p: max(len(p), 7) for p in todos_produtos}
    linha = f"| {'Usuário':<{col_user_width}} "
    for p in todos_produtos:
        linha += f"| {p:^{col_prod_widths[p]}} "
    linha += "|"
    print("+" + "-"*(len(linha)-2) + "+")
    print(linha)
    print("+" + "-"*(len(linha)-2) + "+")
    for u, produtos in usuarios.items():
        linha = f"| {u:<{col_user_width}} "
        for p in todos_produtos:
            val = produtos.get(p, "-")
            linha += f"| {val:^{col_prod_widths[p]}} "
        linha += "|"
        print(linha)
    print("+" + "-"*(len(linha)-2) + "+")

def tabela_recomendacoes():
    if not usuarios:
        print("Nenhum usuário adicionado.")
        return
    col_user_width = max(len("Usuário"), max(len(u) for u in usuarios))
    col_item_width = 20
    linha = f"| {'Usuário':<{col_user_width}} | {'Top 1':<{col_item_width}} | {'Top 2':<{col_item_width}} | {'Top 3':<{col_item_width}} |"
    print("+" + "-"*(len(linha)-2) + "+")
    print(linha)
    print("+" + "-"*(len(linha)-2) + "+")
    for u in usuarios:
        recs = recomendar(u)
        top = []
        for item, score in recs:
            barra_len = int(score*2)
            barra = "█"*barra_len
            top.append(f"{item} {score} {barra}")
        while len(top) < 3:
            top.append("-")
        linha = f"| {u:<{col_user_width}} | {top[0]:<{col_item_width}} | {top[1]:<{col_item_width}} | {top[2]:<{col_item_width}} |"
        print(linha)
    print("+" + "-"*(len(linha)-2) + "+")

def menu():
    while True:
        print("\n1 - Adicionar usuário/produto")
        print("2 - Ver tabela de usuários e produtos")
        print("3 - Ver recomendações automáticas")
        print("4 - Sair")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            adicionar()
        elif opcao == "2":
            tabela_usuarios()
        elif opcao == "3":
            tabela_recomendacoes()
        elif opcao == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida")

if __name__ == "__main__":
    menu()
