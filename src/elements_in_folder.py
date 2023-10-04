import os

def get_folder_items(directorio):
    nombres_elementos = []
    
    # Recorre el contenido del directorio
    for nombre in os.listdir(directorio):
        ruta = os.path.join(directorio, nombre)
        
        if nombre == 'storeInfo.txt':
            tempDict = {'name': nombre,
                        'type': 'storeInfo'}
            nombres_elementos.append(tempDict)
            
        # Verifica si es una carpeta o un archivo
        elif os.path.isdir(ruta):

            tempDict = {'name': nombre,
                        'type': 'directory'}
            
            nombres_elementos.append(tempDict)
            newDirectory = directorio + "/" + nombre
            for file in get_folder_items(newDirectory):
                nombres_elementos.append(file)
            
        elif os.path.isfile(ruta):
            tempDict = {'name': nombre,
                        'type': 'file',
                        'indentation' : 2}
            
            nombres_elementos.append(tempDict)
    
    return nombres_elementos

# Ejemplo de uso
#directorio = r"/home/nos/Documents/Works/Datos02-Proyecto-03/env"  # Reemplaza con la ruta de tu directorio
#elementos = get_folder_items(directorio)
#elementos = get_folder_items(directorio)
#print(elementos)