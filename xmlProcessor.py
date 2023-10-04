from xml.dom import minidom
import os
from src.separador import separar_variable

#create xml document with some elements
def insert(path, attributeList, valueList):
    xml = minidom.Document()
    i = 0

    #Saving the attributes of the instance
    archive = path + "/storeInfo.txt"
    with open(archive, 'r') as file:
        for linea in file:
            attribute = linea.split(",") 

    #create the root node (the first node of the tree)
    #each element it's a node of the tree
    root = xml.createElement(valueList[0])
    xml.appendChild(root) #adding the root node to the tree

    for originallAttribute in attribute:
        childNode = xml.createElement(originallAttribute)
        root.appendChild(childNode)
        if i < len(attributeList):
            if originallAttribute == attributeList[i]:
                text = xml.createTextNode(valueList[i])
                childNode.appendChild(text)
                i = i+1

    #Convert the document to a string 
    #This part is for formatting purposes
    xml_str = xml.toprettyxml(indent="  ")

    #Saving the file to a specific path 
    directory = path
    fileName = valueList[0] + ".xml"
    file_path = os.path.join(directory, fileName)

    #Save the xml file
    with open(file_path, "w") as f:
        f.write(xml_str)
    

def deleteAllInstances(path):
    for file in os.listdir(path):
        if file != "storeInfo.txt":
            file_path = os.path.join(path, file)  # get the complete path
            if os.path.exists(file_path):  
                os.remove(file_path) 

def auxiliarWhere(XMLStorePath, condition): #function to obtain all the coincidences
    results = []
    atribute = condition[0]
    value = condition[1]

    archives = os.listdir(XMLStorePath)

    for file in archives:
        if file.endswith(".xml"):
            
            path = os.path.join(XMLStorePath, file) #getting the file path

            dom = minidom.parse(path)

            root = dom.documentElement

            childs = root.getElementsByTagName(atribute)

            for child in childs:
                if child.firstChild.nodeValue == value:
                    results.append(path)
                    break
    
    return results

def removeCoincidences(coincidenceList):
    for coincidence in coincidenceList:
        if os.path.exists(coincidence):  
            os.remove(coincidence) 

def updateCoincidences(coincidenceList, listOfChanges):
    for coincidence in coincidenceList:
        dom = minidom.parse(coincidence)
        root = dom.documentElement

        for change in listOfChanges:
            changes = separar_variable(change, '=')
            attribute = changes[0]
            value = changes[1]

            childs = root.getElementsByTagName(attribute)

            for child in childs:
                    child.firstChild.nodeValue = value

        with open(coincidence, 'w') as file:
                dom.writexml(file)

def threeConditionWhere(XMLStorePath, conditions):
    results = []
    operator1 = conditions[1]
    operator2 = conditions[3]

    condition1 = conditions[0]
    parameters1 = separar_variable(condition1,"=")
    condition2 = conditions[2]
    parameters2 = separar_variable(condition2,"=")
    condition3 = conditions[4]
    parameters3 = separar_variable(condition3,"=")

    archives = os.listdir(XMLStorePath)

    for file in archives:
        if file.endswith(".xml"):
            
            path = os.path.join(XMLStorePath, file) #getting the file path

            dom = minidom.parse(path)
            root = dom.documentElement

            childs = root.getElementsByTagName('*')

            #condition variables
            cond1_state = False
            cond2_state = False
            cond3_state = False

            #first condition
            for child in childs:
                if child.firstChild.nodeValue == parameters1[1]:
                    cond1_state = True
                    break
            
            #second condition
            for child in childs:
                if child.firstChild.nodeValue == parameters2[1]:
                    cond2_state = True
                    break
                
            #third condition
            for child in childs:
                if child.firstChild.nodeValue == parameters3[1]:
                    cond3_state = True
                    break
            
            #checkin with operators
            if operator1 == 'AND' and operator2 == 'AND':
                if (cond1_state and cond2_state) and cond3_state:
                    results.append(path)

            if operator1 == 'AND' and operator2 == 'OR':
                if (cond1_state and cond2_state) or cond3_state:
                    results.append(path)

            if operator1 == 'OR' and operator2 == 'AND':
                if (cond1_state or cond2_state) and cond3_state:
                    results.append(path)

            if operator1 == 'OR' and operator2 == 'OR':
                if (cond1_state or cond2_state) or cond3_state:
                    results.append(path)

    return results

def twoConditionWhere(XMLStorePath, conditions):
    results = []
    operator = conditions[1]

    condition1 = conditions[0]
    parameters1 = separar_variable(condition1, "=")
    condition2 = conditions[2]
    parameters2 = separar_variable(condition2, "=")

    archives = os.listdir(XMLStorePath)

    for file in archives:
        if file.endswith(".xml"):
            path = os.path.join(XMLStorePath, file)  # Obtener la ruta completa del archivo

            dom = minidom.parse(path)
            root = dom.documentElement

            childs = root.getElementsByTagName('*')

            # Variables de condición
            cond1_state = False
            cond2_state = False

            # Primera condición
            for child in childs:
                if child.firstChild.nodeValue == parameters1[1]:
                    cond1_state = True
                    break

            # Segunda condición
            for child in childs:
                if child.firstChild.nodeValue == parameters2[1]:
                    cond2_state = True
                    break

            # Verificación con el operador
            if operator == 'AND':
                if cond1_state and cond2_state:
                    results.append(path)
            elif operator == 'OR':
                if cond1_state or cond2_state:
                    results.append(path)

    return results

def generateSelectDict(attList, coincidenceList):

    data = {}

    for file in coincidenceList:
        dom = minidom.parse(file)
        root = dom.documentElement
        row = {}

        for attribute in attList:
            childs = root.getElementsByTagName(attribute)

            if childs:
                # Si se encuentra el atributo, se guarda su valor en el diccionario de fila
                value = childs[0].firstChild.nodeValue
                row[attribute] = value
            else:
                # Si no se encuentra el atributo, se guarda None en el diccionario de fila
                row[attribute] = None

        data[os.path.basename(file)] = row

    return data