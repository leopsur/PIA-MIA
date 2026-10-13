l=[1,2,2,7,7,2,5,1,3,4,5,6,7,8,9,10]

def contar_aprobados(l):

    contador=0;
    for i in l:
        if(i>=5):
            contador=contador+1;

    print(contador);

def contar_aprobados_v2(l):

    l_aprobados=[]

    for i in l:
        if(i>=5):
            l_aprobados.append(i)

    print(len(l_aprobados))

contar_aprobados(l)
contar_aprobados_v2(l)


"""
def media(l):

def max(l):


def min(l):


"""