# E3.2
import csv
from pathlib import Path

RUTA = Path(__file__).parent / "datos" / "iris.csv"

MEDIDAS=['largo_sep', 'ancho_sep', 'largo_pet', 'ancho_pet']

#Calculos
def obtener_media_columna(filas,columna):

    valores={}

    for fila in filas:
        clase=fila['clase']

        if clase not in valores:
            valores[clase]={}
        valores[clase].append(fila[columna])

    resultados = {}
    for clase,v in valores.items():
        print(clase)
        print(sum(v)/len(v))
        resultados[clase]=valores.items()

    
    #{clase: suma() for v,}





with open(RUTA, newline="") as f:
    filas = list(csv.DictReader(f))

for fila in filas:
    for medida in MEDIDAS:
        fila[medida] = float(fila[medida])


obtener_media_columna(filas,'ancho_sep')



#Comprobacion
print("\n--- COMPROBACION DE DATOS ---")
for fila in filas:
    print(fila)
    #print(fila)
    #print(type(fila["largo_pet"]))


