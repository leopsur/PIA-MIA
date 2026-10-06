listas = [22,33,4,5,4,5,66,7,8,9,99,99]

ver = []
queda = []

for v in listas:
    if v not in ver:
        ver.append(v)
        queda.append(v)


print (f"El resultado es {queda}")