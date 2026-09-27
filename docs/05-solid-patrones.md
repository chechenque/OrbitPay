# Fase 5 — SOLID y patrones de diseño

## Objetivo

En esta fase se integraron principios de diseño orientado a objetos y patrones de diseño para reducir el acoplamiento del motor de pagos de OrbitPay.

La implementación busca reemplazar la lógica monolítica basada en condicionales por una arquitectura basada en abstracciones, composición y polimorfismo.

Los patrones implementados son:

* Factory.
* Strategy.
* Observer.

⸻

## Arquitectura resultante

El procesamiento de un pago sigue el siguiente flujo:

                    PagoEngine
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          ▼             ▼             ▼
       Cuenta      MetodoPago   EstrategiaComision
                        │             │
              ┌─────────┼───────┐     │
              ▼         ▼       ▼     ▼
           Tarjeta Transferencia Wallet
                                      │
                           ┌──────────┴──────────┐
                           ▼                     ▼
                     ComisionFija       ComisionPorcentual
                        │
                        ▼
                  ResultadoPago
                        │
                        ▼
                 GestorEventosPago
                        │
                 ┌──────┴──────┐
                 ▼             ▼
           PagoAprobado   PagoRechazado

El PagoEngine coordina la operación, pero delega responsabilidades a las abstracciones correspondientes.

⸻

## Factory Pattern

Implementación

El patrón Factory está implementado mediante:
```
orbitpay/patterns/factory.py
```
La clase principal es:
```
MetodoPagoFactory
```
Su responsabilidad es crear implementaciones concretas de MetodoPago.

Ejemplo:
```python
metodo = MetodoPagoFactory.crear(
    "tarjeta",
    "**** **** **** 1234",
)
```
El código cliente recibe un objeto compatible con:

MetodoPago

sin tener que construir directamente una instancia concreta.

Beneficio

La creación de objetos queda separada de la lógica que utiliza dichos objetos.

Esto reduce el acoplamiento entre el código cliente y las implementaciones concretas de los métodos de pago.

⸻

## Strategy Pattern

Implementación

El patrón Strategy está implementado en:
```
orbitpay/patterns/strategy.py
```
La abstracción principal es:

EstrategiaComision

y cuenta con las siguientes estrategias:

ComisionFija
ComisionPorcentual

Ejemplo:
```python
estrategia = ComisionFija(10.0)
comision = estrategia.calcular(500.0)
```
También puede utilizarse:
```python
estrategia = ComisionPorcentual(2.5)
comision = estrategia.calcular(500.0)
```
El PagoEngine depende de:

EstrategiaComision

y no de una estrategia concreta.

Beneficio

Es posible cambiar la forma de calcular la comisión sin modificar el motor de pagos.

Esto favorece:

* Open/Closed Principle.
* Dependency Inversion Principle.
* Polimorfismo.
* Separación de responsabilidades.

⸻

## Observer Pattern

Implementación

El patrón Observer está implementado en:
```
orbitpay/patterns/observer.py
```
Los componentes principales son:

GestorEventosPago
ObservadorPago
PagoAprobado
PagoRechazado
RegistroPagosObserver

El GestorEventosPago mantiene una colección de observadores y los notifica cuando ocurre un evento.

Ejemplo:
```python
gestor = GestorEventosPago()
observador = RegistroPagosObserver()
gestor.suscribir(observador)
```
Cuando el motor procesa un pago:
```python
self._gestor_eventos.notificar(evento)
```
Los observadores reciben el evento mediante:

actualizar(evento)

Beneficio

El motor de pagos no necesita conocer qué acciones adicionales se realizan después de un pago.

Esto permite incorporar nuevos observadores sin modificar el procesamiento principal.

⸻

## Principios SOLID aplicados

### S — Single Responsibility Principle

Las responsabilidades principales están separadas:

- Componente	Responsabilidad
- Cuenta	Administrar saldo
- Transaccion	Representar una operación
- MetodoPago	Definir el contrato de procesamiento
- MetodoPagoFactory	Crear métodos de pago
- EstrategiaComision	Calcular comisiones
- GestorEventosPago	Gestionar notificaciones
- PagoEngine	Coordinar el proceso de pago

Cada componente tiene un propósito específico.

⸻

### O — Open/Closed Principle

Las estrategias de comisión permiten incorporar nuevas formas de cálculo mediante nuevas implementaciones de:

EstrategiaComision

Por ejemplo, podría agregarse posteriormente:

ComisionPromocional

sin modificar el código que utiliza la estrategia.

De manera similar, pueden incorporarse nuevos métodos de pago implementando:

MetodoPago

⸻

### L — Liskov Substitution Principle

Las clases:

Tarjeta
Transferencia
Wallet

pueden utilizarse donde se espera:

MetodoPago

El motor no necesita conocer cuál implementación concreta recibió.

⸻

### I — Interface Segregation Principle

La abstracción MetodoPago mantiene un contrato pequeño:
```python
procesar(monto)
```
Las implementaciones no están obligadas a implementar operaciones que no necesitan.

⸻

### D — Dependency Inversion Principle

PagoEngine depende de abstracciones:

- MetodoPago
- EstrategiaComision
- EventoPago

en lugar de depender directamente de implementaciones concretas.

Por ejemplo:
```python
def procesar_pago(
    self,
    cuenta: Cuenta,
    metodo_pago: MetodoPago,
    transaccion: Transaccion,
) -> ResultadoPago:
```
El motor recibe una abstracción y utiliza polimorfismo.

⸻

## Prevención del doble cobro

Uno de los problemas originales del sistema era la posibilidad de procesar dos veces una misma operación.

El PagoEngine mantiene un conjunto de identificadores:
```python
self._transacciones_procesadas: set[str]
```
Antes de procesar una operación se verifica:
```python
if transaccion.id in self._transacciones_procesadas:
    raise ValueError(...)
```
Después de procesar correctamente o rechazar la operación, el identificador queda registrado.

Esto implementa una estrategia de idempotencia dentro del alcance del prototipo.

La prueba correspondiente verifica que una misma transacción no pueda descontar el saldo dos veces.

⸻

## Evidencia de pruebas

Los patrones cuentan con pruebas unitarias y el motor cuenta con pruebas de integración.

Se verifican:

* creación de métodos de pago;
* comportamiento polimórfico;
* cálculo de comisiones;
* validación de comisiones;
* suscripción de observadores;
* eliminación de observadores;
* notificación de eventos;
* pagos aprobados;
* pagos rechazados;
* saldo insuficiente;
* prevención del doble procesamiento.

La calidad del código se valida mediante:
```bash
python -m pytest
python -m pytest --cov=orbitpay --cov-report=term-missing
python -m ruff check .
python -m black --check .
python -m mypy --strict orbitpay/
```
⸻

## Resultado de la fase

La arquitectura dejó de depender de una única lógica monolítica y pasó a utilizar composición, abstracciones y polimorfismo.

Los tres patrones requeridos quedaron integrados en el dominio:

| Patrón | Componente principal | Propósito |
|--------|----------------------|-----------|
| Factory | MetodoPagoFactory | Creación de métodos de pago |
| Strategy | EstrategiaComision | Cálculo intercambiable de comisiones |
| Observer | GestorEventosPago | Notificación desacoplada de eventos |

La implementación proporciona una base preparada para la siguiente fase: testing, refactorización y evaluación de calidad.