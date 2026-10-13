#Calcular el area de una figura, cuadrado, circulo y perimetro.

from abc import ABC, abstractmethod
from math import pi

class Figura(ABC):

    @abstractmethod
    def area(self): ...

class Circulo(Figura):
    def __init__(self, radio):
        self.radio = radio

    def area(self):
        return round(pi * self.radio ** 2,2)


mi_circulo = Circulo(radio=5)

resultado_area= mi_circulo.area()

print(resultado_area)


