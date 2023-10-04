from heapq import heappop, heappush
from collections import Counter

class NodoHuffman:
    def __init__(self, valor, frecuencia):
        self.valor = valor
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

def obtener_frecuencias(texto):
    frecuencias = Counter(texto)
    return frecuencias

def construir_arbol(frecuencias):
    heap = []
    for valor, frecuencia in frecuencias.items():
        nodo = NodoHuffman(valor, frecuencia)
        heappush(heap, nodo)

    while len(heap) > 1:
        nodo_izq = heappop(heap)
        nodo_der = heappop(heap)
        nodo_padre = NodoHuffman(None, nodo_izq.frecuencia + nodo_der.frecuencia)
        nodo_padre.izquierda = nodo_izq
        nodo_padre.derecha = nodo_der
        heappush(heap, nodo_padre)

    return heap[0]

def construir_diccionario_codigos(arbol, prefijo="", diccionario_codigos={}):
    if arbol.valor is not None:
        diccionario_codigos[arbol.valor] = prefijo
    else:
        construir_diccionario_codigos(arbol.izquierda, prefijo + "0", diccionario_codigos)
        construir_diccionario_codigos(arbol.derecha, prefijo + "1", diccionario_codigos)

    return diccionario_codigos

def comprimir_texto(texto):
    frecuencias = obtener_frecuencias(texto)
    arbol = construir_arbol(frecuencias)
    diccionario_codigos = construir_diccionario_codigos(arbol)
    texto_comprimido = ""

    for caracter in texto:
        texto_comprimido += diccionario_codigos[caracter]

    return texto_comprimido

def descomprimir_texto(texto_comprimido, arbol):
    texto_descomprimido = ""
    nodo_actual = arbol

    for bit in texto_comprimido:
        if bit == "0":
            nodo_actual = nodo_actual.izquierda
        else:
            nodo_actual = nodo_actual.derecha

        if nodo_actual.valor is not None:
            texto_descomprimido += nodo_actual.valor
            nodo_actual = arbol

    return texto_descomprimido



