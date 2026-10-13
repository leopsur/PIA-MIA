rechazos = []

for n, fila in enumerate(filas, start=2):
    
    try:
        limpia = limpiar(fila)
        
    except (ValueError, KeyError) as e:
        rechazos.append({"linea": n, "motivo": str(e)})
        continue
    
    validas.append(limpia)