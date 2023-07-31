import sqlite3
from classes import *

criar_tabela_contas()
criar_tabela_movimentos()
caixa = CaixaMultibanco()

while True:
    print("--- Multibanco ---")
    nome_conta = input("Escolha a conta (Leo ou Goncalo): ")
    conta = caixa.selecionar_conta(nome_conta)
    if conta:
        break
    else:
        print("Erro. Conta não encontrada")

while True:
    print(f"\n--- Bem-vindo, {conta.nome}. ---")
    print("1. Retirar dinheiro")
    print("2. Depositar dinheiro")
    print("3. Transferir dinheiro")
    print("4. Consultar extrato")
    print("0. Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        valor = float(input("Digite o valor a retirar: "))
        print(caixa.retirar_dinheiro(conta, valor))
    elif opcao == "2":
        valor = float(input("Digite o valor a depositar: "))
        print(caixa.depositar_dinheiro(conta, valor))
    elif opcao == "3":
        destino = input("Digite o nome da conta de destino (Leo ou Goncalo): ")
        conta_destino = caixa.selecionar_conta(destino)
        if conta_destino:
            valor = float(input("Digite o valor a transferir: "))
            print(caixa.transferir_dinheiro(conta, conta_destino, valor))
        else:
            print("Conta de destino não encontrada.")
    elif opcao == "4":
        print(caixa.consultar_extrato(conta))
    elif opcao == "0":
        break
    else:
        continue