y = [x for x in range(5)]
print(y)

x = [y for y in range(0,12,2)]
print(x)

print([n for n in range(11) if n % 2 == 1])

pessoas = [' Ana ', 'manuela', 'FELIpe', 'PedrO']

ana = 'Ana  '
print(ana)

print(ana.lower())

pessoas_normalizadas = [pessoa.strip().capitalize() for pessoa in pessoas]
print(pessoas_normalizadas)