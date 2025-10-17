import functools

def meu_decorador(funcao):
    @functools.wraps(funcao)
    def func_que_roda_funcao():
        print("*****Embrulhando função no decorador!******")
        funcao()
        print("*****Fechando embrulho!******")
    return func_que_roda_funcao

@meu_decorador
def minha_funcao():
    print("Eu Sou uma Função!")

print(minha_funcao())