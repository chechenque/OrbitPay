# Herencia y Polimorfismo

## Objetivo

Esta fase implementa los conceptos de abstracción, herencia y polimorfismo dentro del dominio de métodos de pago de OrbitPay OO.

El objetivo principal es permitir que el motor procese diferentes métodos de pago mediante un contrato común, evitando que la lógica principal dependa de clases concretas.

⸻

## Abstracción MetodoPago

Los métodos de pago comparten una operación fundamental:
```python
procesar(monto: float) -> bool
```
Para definir este contrato se creó la clase abstracta:
```python
class MetodoPago(ABC):
    @abstractmethod
    def procesar(self, monto: float) -> bool: ...
```
La clase funciona como una abstracción que establece qué comportamiento debe proporcionar cualquier método de pago.

⸻

## Herencia

Los métodos concretos heredan de MetodoPago:
```text
MetodoPago
├── Tarjeta
├── Transferencia
└── Wallet
```
Cada implementación proporciona su propia versión de:
```python
procesar()
```
Esto permite compartir un contrato común manteniendo implementaciones independientes.

⸻

## Implementaciones concretas

### Tarjeta

Representa un pago mediante tarjeta:

Su implementación recibe un identificador de tarjeta enmascarado.

⸻

### Transferencia

Representa una operación mediante transferencia bancaria:

Utiliza un identificador de cuenta bancaria.

⸻

### Wallet

Representa un pago mediante una billetera digital:

Utiliza el proveedor correspondiente como identificador.

⸻

## Polimorfismo

El PagoEngine no recibe una tarjeta, transferencia o wallet específicamente.

Recibe:
```python
metodo_pago: MetodoPago
```
y posteriormente ejecuta:
```python
metodo_pago.procesar(total)
```
El mismo código puede trabajar con diferentes implementaciones.

Por ejemplo:
```python
engine.procesar_pago(
    cuenta=cuenta,
    metodo_pago=Tarjeta("**** **** **** 1234"),
    transaccion=transaccion,
)
```
o:
```python
engine.procesar_pago(
    cuenta=cuenta,
    metodo_pago=Transferencia("0123456789"),
    transaccion=transaccion,
)
```
o:
```python
engine.procesar_pago(
    cuenta=cuenta,
    metodo_pago=Wallet("OrbitWallet"),
    transaccion=transaccion,
)
```
La lógica del motor permanece igual.

⸻

## Ausencia de lógica basada en tipos

Una de las decisiones importantes de diseño fue evitar una implementación basada en condiciones como:
```python
if tipo == "tarjeta":
    ...
elif tipo == "transferencia":
    ...
elif tipo == "wallet":
    ...
```
o:
```python
isinstance(metodo_pago, Tarjeta)
```
para determinar cómo procesar un pago.

En su lugar, se utiliza polimorfismo.

El objeto concreto conoce cómo realizar su propia operación mediante:
```python
procesar()
```
⸻

## Factory y polimorfismo

El patrón Factory complementa esta arquitectura.

La Factory crea una instancia concreta:
```python
MetodoPagoFactory.crear(
    "tarjeta",
    "**** **** **** 1234",
)
```
pero devuelve el contrato abstracto:

MetodoPago

Esto permite separar:
```text
creación del objeto
        ↓
implementación concreta
        ↓
uso mediante abstracción
```
El consumidor no necesita conocer cómo fue construida la instancia.

⸻

## Extensibilidad

La arquitectura permite incorporar nuevos métodos de pago.

Por ejemplo, puede registrarse una nueva implementación:
```python
class Criptomoneda(MetodoPago): ...
```
y posteriormente registrarse en la Factory:
```python
MetodoPagoFactory.registrar(
    "criptomoneda",
    Criptomoneda,
)
```
El PagoEngine no necesita modificarse.

Esto demuestra la aplicación conjunta de:

* Abstracción.
* Herencia.
* Polimorfismo.
* Factory.
* Open/Closed Principle.

⸻

## Relación con SOLID

La utilización de una abstracción común permite aplicar varios principios SOLID.

### Liskov Substitution Principle

Las implementaciones concretas de MetodoPago pueden sustituir a la abstracción sin que PagoEngine tenga que cambiar.

### Open/Closed Principle

Nuevos métodos de pago pueden incorporarse sin modificar el algoritmo central del motor.

### Dependency Inversion Principle

El motor depende del contrato MetodoPago, no de una implementación específica.

⸻

## Validación mediante pruebas

La suite de pruebas comprueba:

* Creación de tarjetas.
* Creación de transferencias.
* Creación de wallets.
* Implementación del contrato MetodoPago.
* Procesamiento mediante el método común.
* Rechazo de montos inválidos.
* Uso de métodos de pago dentro de PagoEngine.
* Registro de nuevos métodos mediante Factory.

Estas pruebas permiten verificar que las implementaciones respetan el contrato establecido.

⸻

## Resultado

La arquitectura de métodos de pago permite que OrbitPay procese diferentes formas de pago mediante una abstracción común.

La combinación de herencia y polimorfismo evita acoplar el motor a implementaciones concretas y facilita la incorporación de nuevos métodos.

Esta decisión arquitectónica constituye una base para la aplicación posterior de Factory, Strategy, Observer y principios SOLID.