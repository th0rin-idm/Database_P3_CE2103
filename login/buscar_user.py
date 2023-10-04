def buscar_en_txt(variable):
    ruta_archivo = r"/home/nos/Documents/Works/Datos02-Proyecto-03/login/users.txt"
    #ruta_archivo = r"C:\Users\ignac\Downloads\Datos02-Proyecto-03-main\login\users.txt"

    with open(ruta_archivo, "r") as archivo:
        for linea in archivo:
            if variable in linea:
                return True  # La variable fue encontrada en el archivo

    return False  # La variable no fue encontrada en el archivo


