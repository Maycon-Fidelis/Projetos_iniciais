import datetime

class Funcionario():
    aumento = 1.04
    def __init__(self,nome,salario):
        self.nome = nome
        self.salario = salario

    def dados(self):
        return {'nome': self.nome, "salario": self.salario}
    
    def aplicar_aumento(self):
        self.salario = self.salario * self.aumento

    @classmethod
    def definir_novo_aumento(cls,novo_aumento):
        cls.aumento = novo_aumento

    @staticmethod
    def dia_util(dia):
        #segunda = 0
        #domingo = 6
        if dia.weekday() == 5 or dia.weekday == 6:
            return False
        return True

fabio = Funcionario('Fabio',7000)

print(fabio.dados())

fabio.aplicar_aumento()

print(fabio.dados())

Funcionario.definir_novo_aumento(1.05)

print(fabio.dados())

fabio.aplicar_aumento()

print(fabio.dados())

pedro = Funcionario('Pedro',8000)

print(pedro.dados())

print(pedro.aplicar_aumento())

print(pedro.dados())

minha_data = datetime.date(2019,4,15) #Quinta

print(Funcionario.dia_util(minha_data))