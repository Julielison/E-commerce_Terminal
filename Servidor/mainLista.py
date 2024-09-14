#from listaSequencial import Lista,ListaError
from Servidor.listaEncadeada import Lista,ListaError

lista = Lista()
print(len(lista))
try:
    for numero in range(10):
        lista.append((numero+1)*10)
    print('Elemento 5:', lista.elemento(5))
    print('Busca:', lista.busca(90))

    for i in range(5):
        print(lista.remover(len(lista)))
    print(len(lista))
    print(lista)

except ListaError as pe:
    print(pe)