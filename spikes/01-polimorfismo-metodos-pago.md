# Spike 01 — Polimorfismo de métodos de pago

## Identificación del riesgo

Riesgo

El sistema inicial podía resolver el procesamiento de pagos mediante
condicionales asociados al tipo concreto de método de pago:
```
if tipo == "tarjeta":
    ...
elif tipo == "transferencia":
    ...
elif tipo == "wallet":
    ...
```
Este enfoque genera acoplamiento entre el motor de pagos y las
implementaciones concretas.

Además, cada nuevo método de pago requeriría modificar el código existente
del motor, aumentando el riesgo de regresiones y dificultando la aplicación
del principio Open/Closed.

Impacto

Medio-alto.

El problema afecta directamente la extensibilidad del sistema y la
separación de responsabilidades.

⸻

## Pregunta técnica

¿Es posible diseñar el procesamiento de pagos para que PagoEngine pueda
trabajar con diferentes métodos de pago sin conocer sus clases concretas?

⸻

## Hipótesis

Si los diferentes métodos de pago implementan una abstracción común
MetodoPago, entonces PagoEngine podrá depender únicamente de dicha
abstracción y utilizar polimorfismo para procesar cualquier implementación
compatible.

Esto permitiría incorporar nuevos métodos de pago sin modificar la lógica
principal del motor.

⸻

## Experimento

Se creó una clase abstracta que define el contrato común:
```python
from abc import ABC, abstractmethod


class MetodoPago(ABC):
    @abstractmethod
    def procesar(self, monto: float) -> bool:
        raise NotImplementedError
```
Posteriormente se implementaron tres métodos concretos:
```text
MetodoPago
├── Tarjeta
├── Transferencia
└── Wallet
```
Cada implementación proporciona su propia versión de:
```
procesar(monto)
```
El motor recibe una instancia de la abstracción:
```
def procesar_pago(
    self,
    cuenta: Cuenta,
    metodo_pago: MetodoPago,
    transaccion: Transaccion,
) -> ResultadoPago:
    ...
```
Por lo tanto, PagoEngine no necesita comprobar si el objeto recibido es
una tarjeta, una transferencia o una wallet.

⸻

## Validación

Se realizaron pruebas para comprobar:

* Que MetodoPago sea una clase abstracta.
* Que Tarjeta implemente correctamente el contrato.
* Que Transferencia implemente correctamente el contrato.
* Que Wallet implemente correctamente el contrato.
* Que las tres implementaciones puedan utilizarse mediante la misma
    abstracción.
* Que el PagoEngine pueda procesar diferentes métodos de pago.
* Que los montos inválidos sean rechazados.

También se comprobó que la Factory puede crear las implementaciones sin
introducir selección condicional dentro del motor.

⸻

## Resultado

La hipótesis fue validada.

Las implementaciones concretas pueden sustituirse mediante el contrato
MetodoPago, permitiendo que el motor trabaje con diferentes formas de
pago sin depender directamente de sus clases concretas.

La decisión también permite combinar el polimorfismo con el patrón Factory,
utilizando un registro extensible para la creación de métodos de pago.

⸻

## Decisión arquitectónica

Se adopta el uso de:

* MetodoPago como abstracción.
* Tarjeta, Transferencia y Wallet como implementaciones concretas.
* PagoEngine dependiente de MetodoPago.
* MetodoPagoFactory como mecanismo de creación.

La decisión reduce el acoplamiento y permite extender el sistema mediante
nuevas implementaciones compatibles con el contrato.

⸻

## Relación con SOLID

El resultado del spike proporciona evidencia para:

### Open/Closed Principle

El sistema puede incorporar nuevas implementaciones de MetodoPago sin
modificar la lógica principal del PagoEngine.

### Liskov Substitution Principle

Las implementaciones concretas pueden utilizarse donde se espera un
MetodoPago, siempre que respeten su contrato.

### Dependency Inversion Principle

PagoEngine depende de la abstracción MetodoPago y no de las
implementaciones concretas.

⸻

## Evidencia en el repositorio

La decisión puede verificarse en:
```bash
orbitpay/payments/metodo_pago.py
orbitpay/payments/tarjeta.py
orbitpay/payments/transferencia.py
orbitpay/payments/wallet.py
orbitpay/patterns/factory.py
orbitpay/engine.py
tests/unit/
tests/integration/test_engine.py
```
## Estado

Riesgo reducido y decisión adoptada.