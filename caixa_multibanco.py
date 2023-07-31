import sqlite3

# Cria a tabela para armazenar os dados das contas
def criar_tabela_contas():
    conn = sqlite3.connect("contas.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS contas (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            saldo REAL NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()

# Cria a tabela para armazenar o histórico de movimentos
def criar_tabela_movimentos():
    conn = sqlite3.connect("contas.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS movimentos (
            id INTEGER PRIMARY KEY,
            conta TEXT NOT NULL,
            operacao TEXT NOT NULL,
            valor REAL NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


class Conta:
    def __init__(self, nome, saldo):
        self.nome = nome
        self.saldo = saldo

    def __str__(self):
        return f"Conta: {self.nome}, Saldo: {self.saldo:.2f} euros"


class CaixaMultibanco:
    def __init__(self):
        self.contas = []
        self.criar_contas_iniciais()
        self.limite_diario = 2500
        self.limite_saque = 500

    def criar_contas_iniciais(self):
        conn = sqlite3.connect("contas.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contas")
        contas_iniciais = cursor.fetchall()
        if not contas_iniciais:
            cursor.executemany(
                "INSERT INTO contas (nome, saldo) VALUES (?, ?)",
                [("Alice", 3000), ("Bob", 1500)],
            )
            conn.commit()
        conn.close()

    def selecionar_conta(self, nome_conta):
        conn = sqlite3.connect("contas.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contas WHERE nome = ?", (nome_conta,))
        conta_info = cursor.fetchone()
        conn.close()
        if conta_info:
            conta = Conta(conta_info[1], conta_info[2])
            return conta
        else:
            return None

    def levantar_dinheiro(self, conta, valor):
        if valor <= 0:
            return "Operação inválida. O valor a levantar deve ser maior que zero."
        elif valor <= conta.saldo and valor <= self.limite_saque:
            conta.saldo -= valor
            conn = sqlite3.connect("contas.db")
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE contas SET saldo = ? WHERE nome = ?",
                (conta.saldo, conta.nome),
            )
            cursor.execute(
                "INSERT INTO movimentos (conta, operacao, valor) VALUES (?, ?, ?)",
                (conta.nome, "Levantamento", -valor),
            )
            conn.commit()
            conn.close()
            self.atualizar_contas()  # Atualiza a lista de contas
            return f"Foi levantado {valor:.2f} euros da conta {conta.nome}. Saldo atual: {conta.saldo:.2f} euros."
        else:
            return "Operação inválida. Verifique o saldo ou o limite de saque diário."

    def depositar_dinheiro(self, conta, valor):
        if valor <= 0:
            return "Operação inválida. O valor a depositar deve ser maior que zero."
        conta.saldo += valor
        conn = sqlite3.connect("contas.db")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE contas SET saldo = ? WHERE nome = ?", (conta.saldo, conta.nome)
        )
        cursor.execute(
            "INSERT INTO movimentos (conta, operacao, valor) VALUES (?, ?, ?)",
            (conta.nome, "Depósito", valor),
        )
        conn.commit()
        conn.close()
        self.atualizar_contas()  # Atualiza a lista de contas
        return f"Foi depositado {valor:.2f} euros na conta {conta.nome}. Saldo atual: {conta.saldo:.2f} euros."

    def transferir_dinheiro(self, conta_origem, conta_destino, valor):
        if valor <= 0:
            return "Operação inválida. O valor a transferir deve ser maior que zero."
        if valor <= conta_origem.saldo:
            conta_origem.saldo -= valor
            conta_destino.saldo += valor
            conn = sqlite3.connect("contas.db")
            cursor = conn.cursor()
            cursor.executemany(
                "UPDATE contas SET saldo = ? WHERE nome = ?",
                [(conta_origem.saldo, conta_origem.nome), (conta_destino.saldo, conta_destino.nome)],
            )
            cursor.execute(
                "INSERT INTO movimentos (conta, operacao, valor) VALUES (?, ?, ?)",
                (conta_origem.nome, "Transferência (envio)", -valor),
            )
            cursor.execute(
                "INSERT INTO movimentos (conta, operacao, valor) VALUES (?, ?, ?)",
                (conta_destino.nome, "Transferência (recebimento)", valor),
            )
            conn.commit()
            conn.close()
            self.atualizar_contas()  # Atualiza a lista de contas
            return f"Foi transferido {valor:.2f} euros da conta {conta_origem.nome} para a conta {conta_destino.nome}. Saldo atual da conta {conta_origem.nome}: {conta_origem.saldo:.2f} euros. Saldo atual da conta {conta_destino.nome}: {conta_destino.saldo:.2f} euros."
        else:
            return "Operação inválida. Verifique o saldo da conta de origem."

    def consultar_extrato(self, conta):
        extrato = f"Extrato da conta {conta.nome}:\n"
        conn = sqlite3.connect("contas.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM movimentos WHERE conta = ? ORDER BY id DESC", (conta.nome,)
        )
        movimentos = cursor.fetchall()
        for movimento in movimentos:
            operacao = movimento[2]
            valor = movimento[3]
            extrato += f"{operacao}: {valor:.2f} euros\n"
        conn.close()
        return extrato

    def atualizar_contas(self):
        self.contas = []
        conn = sqlite3.connect("contas.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contas")
        contas_info = cursor.fetchall()
        for conta_info in contas_info:
            conta = Conta(conta_info[1], conta_info[2])
            self.contas.append(conta)
        conn.close()


if __name__ == "__main__":
    criar_tabela_contas()
    criar_tabela_movimentos()
    caixa = CaixaMultibanco()

    while True:
        print("== CAIXA MULTIBANCO ==")
        nome_conta = input("Digite o nome da conta (Alice ou Bob): ")
        conta = caixa.selecionar_conta(nome_conta)
        if conta:
            break
        else:
            print("Conta não encontrada. Tente novamente.")

    while True:
        print(f"\n== Bem-vindo, {conta.nome}! ==")
        print("1. Levantar dinheiro")
        print("2. Depositar dinheiro")
        print("3. Transferir dinheiro")
        print("4. Consultar extrato")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            valor = float(input("Digite o valor a levantar: "))
            print(caixa.levantar_dinheiro(conta, valor))
        elif opcao == "2":
            valor = float(input("Digite o valor a depositar: "))
            print(caixa.depositar_dinheiro(conta, valor))
        elif opcao == "3":
            destino = input("Digite o nome da conta de destino (Alice ou Bob): ")
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
            print("Opção inválida. Tente novamente.")
