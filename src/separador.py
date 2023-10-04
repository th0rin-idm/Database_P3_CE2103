def separar_variable(variable, separador):
    resultado = []
    elemento = ""
    
    for caracter in variable:
        if caracter == separador:
            resultado.append(elemento)
            elemento = ""
        else:
            elemento += caracter
    
    resultado.append(elemento)
    return resultado

def prueba():
    variable = input("Ingrese la variable a fragmentar: ")
    print(variable)
    #variable = "Hola,mundo,cómo,estás"

    separador = " "

    resultado = separar_variable(variable, separador)
    print(resultado)
    print(resultado[2])

#prueba()