# Encapsulamiento

## Objetivo

Esta fase aplica el principio de encapsulamiento al dominio de OrbitPay OO.

El objetivo es proteger el estado interno de las entidades y evitar que componentes externos puedan modificar directamente información crítica sin pasar por las reglas de negocio correspondientes.

El encapsulamiento permite que cada objeto sea responsable de mantener la consistencia de su propio estado.

⸻

## Estado crítico identificado

Durante el análisis del dominio se identificaron principalmente dos elementos sensibles:

* El saldo de una Cuenta.
* El estado de una Transaccion.

Estos valores pueden afectar directamente el comportamiento financiero del sistema, por lo que no deben modificarse arbitrariamente desde cualquier componente.

⸻

## Encapsulamiento de Cuenta

La cuenta mantiene su saldo mediante el atributo interno:

_saldo

El acceso al saldo se realiza mediante una propiedad:
```python
@property
def saldo(self) -> float:
    return self._saldo
```
La propiedad permite consultar el saldo sin exponer directamente una operación para modificarlo.

Las operaciones válidas se realizan mediante:
```python
depositar()
retirar()
```
⸻

## Reglas de negocio de Cuenta

La clase Cuenta concentra las validaciones relacionadas con su saldo.

Se impide:

* Crear una cuenta con saldo inicial negativo.
* Depositar cantidades menores o iguales a cero.
* Retirar cantidades menores o iguales a cero.
* Retirar una cantidad superior al saldo disponible.

Cuando el saldo no es suficiente se genera:

InsufficientBalanceError

Esto evita que otras partes del sistema tengan que implementar manualmente las reglas de saldo.

⸻

## Encapsulamiento de Transaccion

La transacción contiene su estado mediante:

_estado

El estado se expone mediante una propiedad de solo lectura:
```python
@property
def estado(self) -> str:
    return self._estado
```
La modificación directa del estado se evita mediante el uso de métodos de dominio:
```python
aprobar()
rechazar()
```
⸻

## Estados válidos

Una transacción puede encontrarse en los siguientes estados:

PENDIENTE
APROBADA
RECHAZADA

La validación se realiza durante la construcción del objeto.

Un estado diferente genera:

ValidationError

Esto evita que se creen transacciones con estados desconocidos para el dominio.

⸻

## Antes y después de la refactorización

Durante el desarrollo se identificó como code smell la posibilidad de modificar directamente el estado de una transacción.

La solución inicial permitía una modificación directa similar a:
```python
transaccion.estado = "APROBADA"
```
La solución refactorizada utiliza:
```python
transaccion.aprobar()
```
o:
```python
transaccion.rechazar()
```
El estado se consulta mediante:

transaccion.estado

pero no se proporciona un setter público.

⸻

## Beneficios

El encapsulamiento implementado proporciona:

* Mayor protección del estado interno.
* Centralización de reglas de negocio.
* Reducción de modificaciones inconsistentes.
* Mayor mantenibilidad.
* Mayor claridad en las operaciones del dominio.
* Menor acoplamiento entre componentes.

El objeto se convierte en responsable de mantener la integridad de su propio estado.

⸻

## Evidencia mediante pruebas

Las pruebas verifican tanto los comportamientos válidos como los casos inválidos.

Entre los escenarios considerados se encuentran:

* Saldo inicial negativo.
* Depósito inválido.
* Retiro inválido.
* Saldo insuficiente.
* Estado de transacción inválido.
* Aprobación de transacciones.
* Rechazo de transacciones.

Las pruebas permiten comprobar que las reglas de encapsulamiento no dependen únicamente del comportamiento esperado durante el uso normal.

⸻

## Relación con otros componentes

El encapsulamiento permite que PagoEngine trabaje con las entidades sin modificar directamente sus atributos internos.

Por ejemplo, el motor utiliza:
```python
cuenta.retirar(total)
```
en lugar de modificar directamente:
```python
cuenta._saldo
```
De manera similar, utiliza:
```python
transaccion.aprobar()
```
en lugar de modificar:
```python
transaccion._estado
```
Esto mantiene las reglas del dominio dentro de las entidades correspondientes.

⸻

## Resultado

La fase permitió establecer límites claros sobre el acceso y modificación del estado interno.

Las entidades Cuenta y Transaccion conservan ahora mayor control sobre sus datos críticos, mientras que el resto de los componentes interactúa con ellas mediante operaciones públicas y explícitas.

El resultado es una implementación más consistente con el principio de encapsulamiento de la programación orientada a objetos.