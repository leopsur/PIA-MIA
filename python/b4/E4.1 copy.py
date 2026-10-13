class CuentaBancaria:
    
    def __init__(self, titular, saldo=0.0):
        self.titular = titular
        self._saldo = saldo

    @property
    def saldo(self):
        """Permite consultar el saldo actual como un atributo de solo lectura."""
        return self._saldo

    def retirar(self, cantidad):
        """Resta la cantidad del saldo si hay fondos suficientes y el monto es positivo."""
        if cantidad <= 0:
            print("La cantidad a retirar debe ser mayor que cero.")
            return False
        
        if cantidad > self._saldo:
            print("Fondos insuficientes para realizar el retiro.")
            return False
            
        self._saldo -= cantidad
        print(f"Retiro exitoso de ${cantidad}. Saldo restante: ${self._saldo}")
        return True

    def ingresar(self,cantidad):

        if cantidad <=0:
            print('Cantidad invalida')
            return False

        self._saldo += cantidad
        return True




c=CuentaBancaria('Pepe',200)

print(c.ingresar(2000))

print(c.saldo)