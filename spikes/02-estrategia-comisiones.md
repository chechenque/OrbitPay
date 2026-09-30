# Spike 02 — Estrategia de comisiones

## Identificación del riesgo

Riesgo

El cálculo de las comisiones podía quedar directamente dentro de
PagoEngine.

Por ejemplo, una implementación rígida podría utilizar diferentes
condicionales:
```
if tipo_comision == "fija":
    ...
elif tipo_comision == "porcentual":
    ...
```
Este diseño haría que el motor tuviera simultáneamente la responsabilidad
de procesar pagos y conocer las diferentes reglas de cálculo.

Impacto

Medio.

El acoplamiento dificultaría incorporar nuevas políticas de comisión y
aumentaría la responsabilidad del motor.

⸻

## Pregunta técnica

¿Es posible separar el algoritmo de cálculo de comisión del procesamiento
del pago para permitir diferentes políticas sin modificar PagoEngine?

⸻

## Hipótesis

Si las diferentes políticas de comisión implementan una estrategia común,
PagoEngine podrá utilizar cualquiera de ellas mediante polimorfismo sin
conocer los detalles de cada algoritmo.

⸻

## Experimento

Se definió una abstracción:
```python
from abc import ABC, abstractmethod


class EstrategiaComision(ABC):
    @abstractmethod
    def calcular(self, monto: float) -> float:
        raise NotImplementedError
```
Se implementaron dos estrategias:
```text
EstrategiaComision
├── ComisionFija
└── ComisionPorcentual
```
Comisión fija
```
ComisionFija(10.0)
```
Para una operación válida, devuelve una comisión fija de 10.0.

Comisión porcentual
```
ComisionPorcentual(2.5)
```
Calcula el porcentaje correspondiente sobre el monto de la operación.

⸻

## Integración con el motor

PagoEngine recibe la estrategia mediante inyección de dependencias:
```python
def __init__(
    self,
    estrategia_comision: EstrategiaComision,
    gestor_eventos: GestorEventosPago,
) -> None: ...
```
El motor solamente solicita:
```python
comision = self._estrategia_comision.calcular(transaccion.monto)
```
Por lo tanto, el motor no necesita conocer qué algoritmo concreto está
realizando el cálculo.

⸻

## Validación

Se realizaron pruebas para comprobar:

* Que EstrategiaComision sea abstracta.
* Que ComisionFija implemente correctamente el contrato.
* Que ComisionPorcentual implemente correctamente el contrato.
* Que las estrategias calculen correctamente sus respectivas comisiones.
* Que se rechacen configuraciones inválidas.
* Que se rechacen montos menores o iguales a cero.
* Que PagoEngine pueda utilizar diferentes estrategias.

⸻

## Resultado

La hipótesis fue validada.

El cálculo de comisión quedó desacoplado del motor de pagos y encapsulado en
estrategias intercambiables.

El motor puede trabajar con diferentes políticas sin modificar su lógica
principal.

⸻

## Decisión arquitectónica

Se adopta el patrón Strategy para representar las políticas de
comisión.

La estructura resultante es:
```text
PagoEngine
    │
    │ depende de
    ▼
EstrategiaComision
    │
    ├── ComisionFija
    │
    └── ComisionPorcentual
```
Las estrategias pueden sustituirse mediante el mismo contrato.

⸻

## Relación con SOLID

### Single Responsibility Principle

El cálculo de comisiones queda separado de la responsabilidad de procesar
pagos.

### Open/Closed Principle

Es posible agregar nuevas estrategias de comisión sin modificar el
algoritmo principal del motor.

### Dependency Inversion Principle

PagoEngine depende de EstrategiaComision, una abstracción, y no de una
política concreta.

⸻

## Evidencia en el repositorio

La decisión puede verificarse en:
```text
orbitpay/patterns/strategy.py
orbitpay/engine.py
tests/unit/patterns/
tests/integration/test_engine.py
docs/05-solid-patrones.md
```
## Estado

Riesgo reducido y decisión adoptada.