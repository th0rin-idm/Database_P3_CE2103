def guardar_en_txt(variable):
    # Ruta completa del archivo
    ruta_archivo = r"/home/nos/Documents/Works/Datos02-Proyecto-03/login/users.txt"
    #ruta_archivo = r"C:\Users\ignac\Downloads\Datos02-Proyecto-03-main\login\users.txt"

    # Abrir el archivo en modo de escritura (si no existe, se creará)
    with open(ruta_archivo, "a") as archivo:
        # Escribir la variable en una nueva línea del archivo
        archivo.write(variable + "\n")


