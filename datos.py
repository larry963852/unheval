import fitz
import os
import json
import string
from unidecode import unidecode
#print(os.getcwd())

newStudents = {}
kindExam = ""
tipoExamen = ""

def pauseAndClear():
    os.system("pause")
    os.system("cls")

def getNewStudent(pdf):
    lineas = []
    aux2 = 0
    
    for numero_pagina in range(pdf.page_count):
        pagina = pdf.load_page(numero_pagina)        
        texto_pagina = pagina.get_text()
        lineas = texto_pagina.split('\n')
    
        aux = 0
        #print(lineas)
        auxiapro = 0
            
        
        for i, linea in enumerate(lineas):
            
            if "RESULTADOS FINALES" in linea and aux2 == 0:
                kindExam = lineas[i]
                print(kindExam)
                translator = str.maketrans('', '', string.punctuation)
                sinPuntuacion = kindExam.translate(translator)
                parte = sinPuntuacion.split()
                if "PREFERENCIAL" in parte:
                    tipoExamen = "PREFERENCIAL"
                elif "GENERAL" in parte:
                    tipoExamen = "GENERAL"
                elif "CEPREVAL" in parte:
                    tipoExamen = "CEPREVAL"

            if "ALCANZO VACANTE" in linea:
                if "NO ALCANZO VACANTE" not in linea:                   
                    if tipoExamen == "PREFERENCIAL" or tipoExamen == "GENERAL":
                        carrera = unidecode(lineas[3])
                        if aux == 0: 
                            print("--------------",carrera,"--------------")
                            # Crear un array para almacenar los a los alumnos que ingresaron por cada carrera
                            newStudents[carrera]= []
                        print(lineas[i - 2])
                        print(lineas[i - 1])
                        # Se agrega el nombre y nota por cada alumno
                        datos_alumno = {
                            "name": lineas[i - 2],
                            "note":lineas[i - 1]
                        }
                        newStudents[carrera].append(datos_alumno)
                        aux += 1
                    elif tipoExamen == "CEPREVAL":
                        auxiapro += 1
                        
        aux2 += 1
        
        if auxiapro > 0:
            for i in range(auxiapro):
                carrera = unidecode(lineas[4])             
                if aux == 0: 
                    print("--------------",carrera,"--------------")
                    # Crear un array para almacenar los a los alumnos que ingresaron por cada carrera
                    newStudents[carrera]= []
                print(lineas[i*4 + 12]) #puesto
                print(lineas[i*4 + 13]) #nombre
                print(lineas[i*4 + 14]) #nota1
                print(lineas[i*4 + 15]) #nota2
                print(lineas[auxiapro*4 + 12 + i*2]) #prom
                print(lineas[auxiapro*4 + 13 + i*2]) #estado
                
                # Se agrega el nombre y nota por cada alumno
                datos_alumno = {
                    "puesto":lineas[i*4 + 12],
                    "name": lineas[i*4 + 13],
                    "nota1":lineas[i*4 + 14],
                    "nota2": lineas[i*4 + 15],
                    "promedio":lineas[auxiapro*4 + 12 + i*2],
                    "estado":lineas[auxiapro*4 + 13 + i*2]
                }
                newStudents[carrera].append(datos_alumno)
                aux += 1

        
    pdf.close()
    pauseAndClear()



if __name__ == "__main__":
    archivo_pdf = "preferencial.pdf"
    documento_pdf = fitz.open(archivo_pdf)
    getNewStudent(documento_pdf)
    # Se crear el json con los datos de los alumnos
    with open("data.json", "w") as file:
        json.dump(newStudents, file, indent=4)
