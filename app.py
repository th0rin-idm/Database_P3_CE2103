from flask import Flask, render_template, request, redirect, url_for
import json
from src.generator import folder_generator
from src.elements_in_folder import get_folder_items
from src.separador import separar_variable
from login.buscar_user import buscar_en_txt
from login.crear_user import guardar_en_txt
from src.checkCommand import commandType
from login.hoffman import descomprimir_texto, comprimir_texto, construir_diccionario_codigos, obtener_frecuencias, construir_arbol

import shutil, os


#inicializando una app
app = Flask(__name__) 

@app.route('/')
def index2():
    return render_template('login.html')

@app.route('/guardar', methods=['POST'])
def guardar_datos():
    usuario = request.form['Nombre']
    password = request.form['pass']

    texto_comprimido = comprimir_texto(password)
    #arbol = construir_arbol(obtener_frecuencias(password))

    #user1 = usuario+","+password
    user1 = usuario+","+texto_comprimido
    found=buscar_en_txt(user1)

    if(found==True):
        return redirect('/2')
    else:
        return redirect('/')
    
@app.route('/xmlStoreCreation', methods=['POST'])
def createXMLStore():
    ##creating the xml store directory
    storeName = request.form['storeName'] # a continuacion se puede hacer lo que se necesite con la variable "nombre"
    folder_generator('temp/temporalFiles/', storeName)

    ##Creating a .txt file to store the xml store attributes
    storeAttributes = request.form['attributes']
    directory = 'temp/temporalFiles/' + storeName
    filePath = os.path.join(directory, 'storeInfo.txt')
    with open(filePath, 'w') as file:
        file.write(storeAttributes)
    return redirect(url_for('index'))
#si estamos desde el main, ejecutamos la app

@app.route('/nueva', methods=['POST'])
def crear_cuenta():
    return render_template('nueva_cuenta.html')

@app.route('/crear', methods=['POST'])
def cuenta_creada():
    usuario = request.form['Name']
    password = request.form['npass']
    
    texto_comprimido = comprimir_texto(password)
    arbol = construir_arbol(obtener_frecuencias(password))
    texto_descomprimido = descomprimir_texto(texto_comprimido, arbol)

    #newuser = usuario+","+password
    newuser = usuario+","+texto_comprimido
    cread=guardar_en_txt(newuser)
    return render_template('login.html')

@app.route('/2')
def index():
    # Reemplaza con la ruta de tu directorio
    directorio = r"/home/nos/Documents/Works/Datos02-Proyecto-03/temp/temporalFiles"  
    #directorio = r"C:\Users\ignac\Downloads\Datos02-Proyecto-03-main\temp\temporalFiles"
    list = get_folder_items(directorio)
    
    path = '/home/nos/Documents/Works/Datos02-Proyecto-03/temp/tempDict.txt'

    with open(path, "r") as f:
        content = f.read()

    dictionary = json.loads(content)

    columns = separar_variable(dictionary["columns"], ",")
    content = []
    data = dictionary["data"]

    for value in data.items():
        subContent = []
        #print(value)
        #agregando nombre
        subContent.append(value[0])
        #print(value[1])
        for subValue in value[1].items():
           subContent.append(subValue[1])
        content.append(subContent)

    print(content)

    data = {    
        'src': list,
        'encabezados': columns,
        'contenidos': content
    }
    
    return render_template('index.html', data=data)

@app.route('/commit', methods=['POST'])
def commit():
    dataPath = './data'
    tempPath = './temp/temporalFiles'
    shutil.rmtree(dataPath)
    shutil.copytree(tempPath, dataPath)
    return redirect(url_for('index'))

@app.route('/commandInterpreter', methods=['POST'])
def interpreter():
    Entry = request.form['command']
    splitedEntry = separar_variable(Entry, ";") #separating the commands from the input
    for command in splitedEntry:
        commandType(separar_variable(command, " ")) #executing each command separately
    
    
    return redirect(url_for('index'))
    #return render_template('index.html')

if __name__ == '__main__':
    ##Creation of temporal files
    dataPath = './data'
    tempPath = './temp/temporalFiles'
    shutil.rmtree(tempPath)
    shutil.copytree(dataPath, tempPath)
    app.run(debug=True, port=5000)
