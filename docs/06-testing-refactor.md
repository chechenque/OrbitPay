# 06 — Testing y Refactorización

## Objetivo

Esta fase tuvo como objetivo validar el comportamiento del dominio y del motor de pagos mediante pruebas automatizadas, así como identificar y corregir problemas de diseño mediante refactorizaciones controladas.

El proceso siguió el principio:

Primero pruebas verdes, después refactorización y nuevamente pruebas verdes.

De esta forma se buscó mejorar la estructura interna del sistema sin alterar su comportamiento funcional.

⸻

## Estrategia de testing

OrbitPay utiliza pytest como framework principal de pruebas.

Las pruebas se organizaron en:
```text
tests/
├── unit/
│   ├── domain/
│   ├── patterns/
│   └── payments/
└── integration/
```
Las pruebas unitarias validan componentes individuales, mientras que las pruebas de integración validan la interacción entre el dominio, los métodos de pago, las estrategias, los eventos y el motor de pagos.

Componentes probados

* Cuenta
* Transaccion
* Suscripcion
* MetodoPago
* Tarjeta
* Transferencia
* Wallet
* MetodoPagoFactory
* ComisionFija
* ComisionPorcentual
* GestorEventosPago
* RegistroPagosObserver
* PagoEngine

⸻

## Casos críticos cubiertos

Se validaron principalmente los siguientes escenarios:

### Cuenta

* Creación con datos válidos.
* Rechazo de identificadores vacíos.
* Rechazo de titulares vacíos.
* Rechazo de saldos iniciales negativos.
* Depósitos válidos.
* Rechazo de montos no positivos.
* Retiros válidos.
* Rechazo de retiros con saldo insuficiente.

### Transacción

* Creación de transacciones válidas.
* Validación de identificadores.
* Validación de montos.
* Validación de estados.
* Aprobación mediante aprobar().
* Rechazo mediante rechazar().
* Protección del estado mediante la propiedad estado.

### Métodos de pago

Se verificó que las implementaciones:

Tarjeta
Transferencia
Wallet

cumplen el contrato definido por:

MetodoPago

y pueden ser utilizadas mediante polimorfismo.

### Factory

Se validó que la Factory:

* Cree tarjetas.
* Cree transferencias.
* Cree wallets.
* Acepte tipos escritos en mayúsculas.
* Rechace tipos no soportados.
* Permita registrar nuevos métodos de pago.
* Rechace tipos vacíos.
* Rechace registros sin tipo.

Esto permite demostrar la extensibilidad de la solución.

### Strategy

Se probaron:

* Comisiones fijas.
* Comisiones porcentuales.
* Validación de configuraciones inválidas.
* Validación de montos inválidos.
* Uso mediante la interfaz común EstrategiaComision.

### Observer

Se validaron:

* Eventos de pago aprobado.
* Eventos de pago rechazado.
* Suscripción de observadores.
* Eliminación de observadores.
* Prevención de suscripciones duplicadas.
* Notificación a múltiples observadores.

### PagoEngine

Se validaron los escenarios principales:

1. Pago aprobado.
2. Pago rechazado por saldo insuficiente.
3. Pago rechazado por el método de pago.
4. Prevención de procesamiento duplicado de una misma transacción.
5. Aplicación de comisión.
6. Actualización del saldo.
7. Cambio de estado de la transacción.
8. Generación de eventos.

⸻

## Refactorización

Durante esta fase se identificaron tres code smells principales.

### Code Smell #1 — Mutación directa del estado

La primera versión permitía modificar directamente el estado de una transacción.

Esto representaba un problema de encapsulamiento porque cualquier componente podía modificar el estado sin pasar por reglas del dominio.

Solución

Se encapsuló el estado:
```python
_estado
```
y se expuso mediante:
```python
@property
def estado(self) -> str: ...
```
Las transiciones se realizan mediante:
```python
aprobar()
rechazar()
```
Esto concentra las operaciones de cambio de estado dentro de la propia entidad.

Beneficio

La entidad Transaccion mantiene mayor control sobre su estado interno y se reduce el riesgo de modificaciones inconsistentes.

⸻

### Code Smell #2 — Factory poco extensible

La primera implementación de la Factory utilizaba un registro interno de tipos que obligaba a modificar la clase cuando se agregaba un nuevo método de pago.

Solución

Se implementó un registro extensible:
```python
MetodoPagoFactory.registrar(
    "criptomoneda",
    Criptomoneda,
)
```
La creación continúa utilizando:
```python
MetodoPagoFactory.crear(
    "criptomoneda",
    "BTC-WALLET-001",
)
```
La Factory ahora permite incorporar nuevos métodos sin modificar la lógica central de creación.

Beneficio

La solución se aproxima al principio Open/Closed, ya que el sistema puede extenderse mediante nuevos registros sin modificar el algoritmo principal de creación.

⸻

### Code Smell #3 — Duplicación en PagoEngine

El motor tenía dos caminos de rechazo con lógica repetida.

Ambos realizaban las mismas operaciones:
```text
marcar transacción como rechazada
        ↓
crear evento
        ↓
notificar observadores
        ↓
registrar transacción procesada
        ↓
devolver resultado
```
Solución

Se extrajo la responsabilidad común al método:
```python
_rechazar_pago()
```
De esta manera, procesar_pago() se concentra en coordinar el flujo general, mientras que _rechazar_pago() encapsula la lógica específica del rechazo.

Beneficio

Se eliminó duplicación y se mejoró la mantenibilidad del código.

Además, cualquier modificación futura relacionada con el rechazo de pagos puede realizarse en un único punto.

⸻

## Validación posterior al refactor

Después de cada refactorización se ejecutaron nuevamente las pruebas automatizadas.

Las principales verificaciones utilizadas fueron:
```bash
python -m pytest
python -m black --check .
python -m ruff check .
python -m mypy --strict orbitpay/
```
La ejecución exitosa de estas herramientas permitió comprobar que las modificaciones mantuvieron el comportamiento existente y conservaron las restricciones de calidad del proyecto.

⸻

## Principios aplicados

Durante esta fase se reforzaron los siguientes principios:

| Principio | Aplicación |
|-----------|------------|
| DRY | Eliminación de lógica duplicada en PagoEngine |
| SRP | Separación de responsabilidades dentro del motor |
| OCP | Factory extensible mediante registro |
| Encapsulamiento | Estado de Transaccion protegido |
| Polimorfismo | Uso de MetodoPago como abstracción |
| Programación contra abstracciones | PagoEngine depende de MetodoPago y EstrategiaComision |
| Refactor seguro | Ejecución de pruebas antes y después de los cambios |

⸻

## Resultado de la fase

La fase de testing y refactorización permitió consolidar una arquitectura más mantenible sin modificar el comportamiento funcional esperado.

Los tres code smells seleccionados fueron corregidos y validados mediante pruebas automatizadas.

El sistema cuenta ahora con:

* Entidades con mayor encapsulamiento.
* Factory extensible.
* Strategy para cálculo de comisiones.
* Observer para eventos.
* Motor de pagos con responsabilidades más claras.
* Validaciones automatizadas.
* Tipado estático mediante mypy --strict.
* Formateo mediante Black.
* Análisis estático mediante Ruff.
* Pruebas automatizadas mediante pytest.

Con esta fase se completa el ciclo de testing → refactorización → validación.