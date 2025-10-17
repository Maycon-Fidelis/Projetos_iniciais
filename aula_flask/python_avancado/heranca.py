class Funcionario():
    def __init__(self,nome,salario):
        self.nome = nome
        self.salario = salario
    
    def dados(self):
        return {'nome': self.nome, 'salario': self.salario}
    
fabio = Funcionario('Fabio',7000)

print(fabio.dados())

class Admin(Funcionario):
    def __init__(self,nome,salario):
        super().__init__(nome,salario)

    def atualizar_dados(self, nome):
        self.nome = nome
        return self.dados()
    
Fernando = Admin('Fernando',1400)

print(Fernando.dados())

Fernando.atualizar_dados('Fernandinho')
print(Fernando.dados())