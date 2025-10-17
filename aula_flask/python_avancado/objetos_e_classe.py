# meu_set = {4,"valor",3,"qualquer"}

# print(meu_set)

# # print(meu_set[0])

# meu_dicionario = [{'nome': 'Ana', 'idade': 80}, {'nome': 'José', 'idade': 45},{'nome':'Maria','idade':10}]

# print(meu_dicionario[0]['nome'])
# print(len(meu_dicionario))

# loteria = {'nome': 'Fulano','numeros':(13,4,53,67,82)}

# # poligonos = []

# print(sum(loteria['numeros']))

class JogadorLoteria:
    def __init__(self,nome):
        self.nome = nome
        self.numero = (13,4,53,67,82)
    
    def total(self):
        return sum(self.numero)
    
jogador_1 = JogadorLoteria('Ana')

jogador_2 = JogadorLoteria('Pedro')

print(jogador_1.nome)
print(jogador_2.nome)

print(jogador_1.numero)
print(jogador_1.total())