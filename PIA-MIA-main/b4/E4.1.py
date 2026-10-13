# E4.1
"""
E4.1 · Clase CuentaBancaria con saldo privado, 
ingresar, retirar (valida saldo suficiente) y 
propiedad saldo de solo lectura.
"""
class CuentaBancaria:
 
    def __init__(self, titular, saldo=0.0):
        self.titular = titular
        self._saldo = saldo
 
    @property
    def saldo(self):
        ...
 
    def retirar(self, cantidad):
        ...