from abc import ABC, abstractmethod
from math import pi

class Figura(ABC):

    @abstractmethod
    def area(self): ...

    @abstractmethod
    def perimetro(self): ...  # Añadimos el perímetro al contrato obligatorio

class Circulo(Figura):
    def __init__(self, radio):
        self.radio = radio

    def area(self):
        return round(pi * self.radio ** 2, 2)

    def perimetro(self):
        return round(2 * pi * self.radio, 2)  # Fórmula: 2 * pi * radio

class Cuadrado(Figura):
    def __init__(self, lado):
        self.lado = lado

    def area(self):
        return round(self.lado ** 2, 2)       # Fórmula: lado^2

    def perimetro(self):
        return round(self.lado * 4, 2)        # Fórmula: lado * 4


# --- COMPROBACIÓN DEL CÍRCULO ---
mi_circulo = Circulo(radio=5)
resultado_area_circulo = mi_circulo.area()
resultado_peri_circulo = mi_circulo.perimetro()

print("Círculo:")
print(f"Área: {resultado_area_circulo}")
print(f"Perímetro: {resultado_peri_circulo}")

print("-" * 20)

# --- COMPROBACIÓN DEL CUADRADO ---
mi_cuadrado = Cuadrado(lado=4)
resultado_area_cuad = mi_cuadrado.area()
resultado_peri_cuad = mi_cuadrado.perimetro()

print("Cuadrado:")
print(f"Área: {resultado_area_cuad}")
print(f"Perímetro: {resultado_peri_cuad}")
