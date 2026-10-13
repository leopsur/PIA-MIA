# E3.2
import csv
from pathlib import Path
 
RUTA = Path(__file__).parent / "datos" / "iris.csv"
MEDIDAS= ['largo_sep', 'ancho_sep', 'largo_pet', 'ancho_pet']


def obtener_media_columna(filas,columna):

    valores={}

    for fila in filas:
        clase=fila["clase"]

        if clase not in valores:
            valores[clase]=[]
        valores[clase].append(fila[columna])

    resultados={}
    for clase,v in valores.items():
        resultados[clase]=round(sum(v)/len(v),2)
    
    
    return resultados




 
with open(RUTA, newline="") as f:
    filas = list(csv.DictReader(f))

# Conversión
for fila in filas:
    for medida in MEDIDAS:
        fila[medida]=float(fila[medida])

for medida in MEDIDAS:
    print(medida,": ",obtener_media_columna(filas,medida))






