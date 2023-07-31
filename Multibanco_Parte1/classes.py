import sqlite3

def criar_tabela_contas():
    conn = sqlite3.connect("multibanco.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS contas (
        id INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        saldo REAL NOT NULL)""")
    conn.commit()
    conn.close()

def criar_tabela_movimentos():
    conn = sqlite3.connect("multibanco.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS movimentos (
        id INTEGER PRIMARY KEY,
        conta TEXT NOT NULL,
        operacao TEXT NOT NULL,
        valor REAL NOT NULL)""")
    conn.commit()
    conn.close()


class Conta:
    def __init__(self, nome, saldo):
        self.nome = nome
        self.saldo = saldo

    def __str__(self):
        return f"Nome: {self.nome}, Saldo: {self.saldo:.2f} euros"


class CaixaMultibanco:
    def __init__(self):
        self.contas = []
        self.criar_contas_iniciais()
        self.limite_diario = 2500
        self.limite_retiro = 500

    def criar_contas_iniciais(self):
        conn = sqlite3.connect("multibanco.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contas")
        contas_iniciais = cursor.fetchall()
        if not contas_iniciais:
            cursor.executemany("INSERT INTO contas (nome, saldo) VALUES (?, ?)",[("Leo", 5000), ("Goncalo", 600)])
            conn.commit()
        conn.close()

    def selecionar_conta(self, nome_conta):
        conn = sqlite3.connect("multibanco.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contas WHERE nome = ?", (nome_conta,))
        conta_info = cursor.fetchone()
        conn.close()
        if conta_info:
            conta = Conta(conta_info[1], conta_info[2])
            return conta
        else:
            return None

    def retirar_dinheiro(self, conta, valor):
        if valor <= 0:
            return "Não pode retirar menos ou igual a 0."
        elif valor <= conta.saldo and valor <= self.limite_retiro:
            conta.saldo -= valor
            conn = sqlite3.connect("multibanco.db")
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE contas SET saldo = ? WHERE nome = ?",
                (conta.saldo, conta.nome),
            )
            cursor.execute("INSERT INTO movimentos (conta, operacao, valor) VALUES (?, ?, ?)",(conta.nome, "Retiro", -valor),
            )
            conn.commit()
            conn.close()
            self.atualizar_contas()  # Atualiza a lista de contas
            return f"Retirou {valor:.2f}€. Novo saldo: {conta.saldo:.2f}€."
        else:
            return "Erro. Limite excedido ou valor inválido."

    def depositar_dinheiro(self, conta, valor):
        if valor <= 0:
            return "Não pode depositar menos ou igual a 0."
        conta.saldo += valor
        conn = sqlite3.connect("multibanco.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE contas SET saldo = ? WHERE nome = ?", (conta.saldo, conta.nome))
        cursor.execute("INSERT INTO movimentos (conta, operacao, valor) VALUES (?, ?, ?)",(conta.nome, "Depósito", valor))
        conn.commit()
        conn.close()
        self.atualizar_contas()  # Atualiza a lista de contas
        return f"Depositou {valor:.2f}€. Novo saldo: {conta.saldo:.2f}€."

    def transferir_dinheiro(self, conta_origem, conta_destino, valor):
        if valor <= 0:
            return "Não pode transferir menos ou igual a 0."
        if valor <= conta_origem.saldo:
            conta_origem.saldo -= valor
            conta_destino.saldo += valor
            conn = sqlite3.connect("multibanco.db")
            cursor = conn.cursor()
            cursor.executemany("UPDATE contas SET saldo = ? WHERE nome = ?",[(conta_origem.saldo, conta_origem.nome), (conta_destino.saldo, conta_destino.nome)],)
            cursor.execute("INSERT INTO movimentos (conta, operacao, valor) VALUES (?, ?, ?)",(conta_origem.nome, "Transferência (envio)", -valor),)
            cursor.execute("INSERT INTO movimentos (conta, operacao, valor) VALUES (?, ?, ?)",(conta_destino.nome, "Transferência (recebimento)", valor),)
            conn.commit()
            conn.close()
            self.atualizar_contas()
            return f"Transferiu {valor:.2f}€ de {conta_origem.nome} para {conta_destino.nome}. Novo saldo da conta {conta_origem.nome}: {conta_origem.saldo:.2f}€. Novo saldo da conta {conta_destino.nome}: {conta_destino.saldo:.2f}€."
        else:
            return "Erro. Dinheiro insuficiente para transferir."

    def consultar_extrato(self, conta):
        extrato = f"Extrato da conta {conta.nome}:\n"
        conn = sqlite3.connect("multibanco.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM movimentos WHERE conta = ? ORDER BY id DESC", (conta.nome,))
        movimentos = cursor.fetchall()
        for movimento in movimentos:
            operacao = movimento[2]
            valor = movimento[3]
            extrato += f"{operacao}: {valor:.2f}€\n"
        conn.close()
        return extrato

    def atualizar_contas(self):
        self.contas = []
        conn = sqlite3.connect("multibanco.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contas")
        contas_info = cursor.fetchall()
        for conta_info in contas_info:
            conta = Conta(conta_info[1], conta_info[2])
            self.contas.append(conta)
        conn.close()