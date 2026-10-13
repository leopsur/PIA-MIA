# E3.2
import csv
from pathlib import Path

RUTA = Path(__file__).parent / "datos" / "iris.csv"

MEDIDAS=['largo_sep', 'ancho_sep', 'largo_pet', 'ancho_pet']

with open(RUTA, newline="") as f:
    filas = list(csv.DictReader(f))

for fila in filas:
    #print(fila)
    for medida in MEDIDAS:
        fila[medida] = float(fila[medida])

#Comprobacion
print("\n--- COMPROBACION DE DATOS ---")
for fila in filas:
    print(fila)
    #print(fila)
    #print(type(fila["largo_pet"]))


