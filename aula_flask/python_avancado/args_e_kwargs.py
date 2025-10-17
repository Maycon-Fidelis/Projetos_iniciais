#args ==> argumentos
#kwargs ==> keywords arguments (argumentos de palavras-chave)

def meu_metodo(arg1,arg2):
    return arg1 + arg2

print(meu_metodo(1,2))

def meu_metodo_longo(arg1,arg2,arg3,arg4,arg5):
    return arg1 + arg2 + arg3 + arg4 + arg5

print(meu_metodo_longo(2,4,5,7,4))

def minha_lista_somada(lista):
    return sum(lista)

#kwargs
def soma_simplificada(*args):
    return sum(args)

print(soma_simplificada(6,3,5,7,4))

def metodos_kwargs(*args,**kwargs):
    print(args)
    print(kwargs)

print(metodos_kwargs(3,'saa',4,'qualquer',nome='Ana',idade=25))
#retorna
#(3, 'saa', 4, 'qualquer')
#{'nome': 'Ana', 'idade': 25}
#A ordem importa pq espera primeiro um arg e após um karg

