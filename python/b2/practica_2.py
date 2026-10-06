l=[1,2,2,7,7,2,5,1,3,4,5,6,7,8,9,10]

vistos=[]
resultados=[]

for i in l:
    if i not in vistos:
        resultados.append(i)
        vistos.append(i)

print(resultados)
