departamentos = {'financeiro':1,'pessoas':2, 'operações':3, 'produto':4}
for n in departamentos:
    print (n, departamentos[n])
total = 0
for n in departamentos:
    total = total + departamentos[n]
print(total)

def analisa_departamento (nome, numero):
    return f"Departamento {nome} tem {numero} pessoas"
# Teste
for n in departamentos:
    resultado = analisa_departamento(n, departamentos[n])
    print(resultado)
