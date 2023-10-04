import os, json
from src.separador import separar_variable
from xmlProcessor import *
directory = '/home/nos/Documents/Works/Datos02-Proyecto-03/temp/temporalFiles'

def commandType(splitedCommand):
    #//////////////////////////////////////////////Insert command//////////////////////////////////////////////
    if splitedCommand[0] + " " + splitedCommand[1] == 'INSERT INTO':
        if splitedCommand[6] == 'VALUES':
            
            for nombre in os.listdir(directory):
                if nombre == splitedCommand[2]:  
                    attributeList = separar_variable(splitedCommand[4], ",")
                    valuesList = separar_variable(splitedCommand[8], ",")

                    #error al insertar solo algunos parametros, es decir, si queda uno en medio sin llenar no llena el resto que sigue
                    insert(directory + "/" + splitedCommand[2], attributeList, valuesList)
    
    #////////////////////////////////////////////Delete command////////////////////////////////////////////////
    elif splitedCommand[0] + " " + splitedCommand[1] == 'DELETE FROM':
        if len(splitedCommand) == 3:
            deleteAllInstances(directory + "/" + splitedCommand[2])
        else:
            if splitedCommand[3] == 'WHERE':
                #the "2" index store the xmlstore, the "4" index store the condition
                coincidences = auxiliarWhere(directory + "/" + splitedCommand[2],separar_variable(splitedCommand[4],"="))
                removeCoincidences(coincidences)
    
    
    #////////////////////////////////////////////update command////////////////////////////////////////////////   
    elif splitedCommand[0] == 'UPDATE':
        if splitedCommand[2] == 'SET' and splitedCommand[4] == 'WHERE':
            coincidences = auxiliarWhere(directory + "/" + splitedCommand[1], separar_variable(splitedCommand[5], "="))
            updateCoincidences(coincidences, separar_variable(splitedCommand[3], ','))
    
    #////////////////////////////////////////////select command//////////////////////////////////////////////// 
    elif splitedCommand[0] == 'SELECT':
        if splitedCommand[2] == 'FROM' and splitedCommand[4] == 'WHERE':

            data = {}
            columns = "name,"+splitedCommand[1]
            data["columns"] = columns

            if len(splitedCommand) == 10:
                coincidences = threeConditionWhere(directory + "/" + splitedCommand[3], [splitedCommand[5], splitedCommand[6], splitedCommand[7], splitedCommand[8], splitedCommand[9]])
                print(generateSelectDict(separar_variable(splitedCommand[1], ","), coincidences))
                
                data["data"] = generateSelectDict(separar_variable(splitedCommand[1], ","), coincidences)
                
            elif len(splitedCommand) == 8:
                coincidences = twoConditionWhere(directory + "/" + splitedCommand[3], [splitedCommand[5], splitedCommand[6], splitedCommand[7]])
                print(generateSelectDict(separar_variable(splitedCommand[1], ","), coincidences))

                data["data"] = generateSelectDict(separar_variable(splitedCommand[1], ","), coincidences)
            
            elif len(splitedCommand) == 6:
                coincidences = auxiliarWhere(directory + "/" + splitedCommand[3], separar_variable(splitedCommand[5],"="))
                print(generateSelectDict(separar_variable(splitedCommand[1], ","), coincidences))

                data["data"] = generateSelectDict(separar_variable(splitedCommand[1], ","), coincidences)


            #saving the dictionary to txt file
            txtPath = "/home/nos/Documents/Works/Datos02-Proyecto-03/temp/tempDict.txt"

            with open(txtPath, 'w') as file:
                json.dump(data, file)

    return False
