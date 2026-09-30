# Cierre del Proyecto

## Objetivo del cierre

Esta fase consolida los resultados obtenidos durante el desarrollo de OrbitPay OO y verifica que el proyecto cuente con los elementos técnicos, documentales y de calidad necesarios para preparar su entrega final.

El desarrollo se realizó mediante ciclos de la Metodología Espiral, incorporando progresivamente modelado, análisis de riesgos, encapsulamiento, herencia, polimorfismo, principios SOLID, patrones de diseño, testing y refactorización.

⸻

## Estado final de la solución

OrbitPay OO es un motor de pagos y suscripciones desarrollado en Python mediante programación orientada a objetos.

La solución implementa una arquitectura separada por responsabilidades:
```text
orbitpay/
├── domain/
│   ├── cuenta.py
│   ├── exceptions.py
│   ├── suscripcion.py
│   └── transaccion.py
│
├── payments/
│   ├── metodo_pago.py
│   ├── tarjeta.py
│   ├── transferencia.py
│   └── wallet.py
│
├── patterns/
│   ├── factory.py
│   ├── observer.py
│   └── strategy.py
│
└── engine.py
```
La separación permite mantener independientes las entidades del dominio, los métodos de pago, los patrones de diseño y la coordinación del procesamiento.

⸻

## Funcionalidad implementada

El sistema permite representar:

* Cuentas de usuarios.
* Transacciones.
* Suscripciones.
* Métodos de pago.
* Comisiones.
* Eventos de pago.
* Procesamiento de pagos.
* Rechazos por saldo insuficiente.
* Rechazos por métodos de pago.
* Prevención de procesamiento duplicado.

El flujo principal de un pago es:
```text
Cuenta
   │
   ├── Transacción
   │
   ├── Método de pago
   │
   └── Estrategia de comisión
           │
           ▼
      PagoEngine
           │
      ┌────┴────┐
      ▼         ▼
  Aprobado   Rechazado
      │         │
      └────┬────┘
           ▼
      Evento de pago
           │
           ▼
       Observer
```
⸻

## Programación orientada a objetos

El proyecto utiliza los principales mecanismos de programación orientada a objetos solicitados.

### Encapsulamiento

Los estados críticos se mantienen protegidos mediante atributos internos y propiedades.

Ejemplo:
```python
@property
def estado(self) -> str:
    return self._estado
```
Las modificaciones se realizan mediante métodos de dominio como:
```python
aprobar()
rechazar()
```
Esto evita que componentes externos modifiquen directamente el estado interno de una transacción.

⸻

### Herencia

Los métodos de pago concretos implementan la abstracción:

MetodoPago

mediante:

- Tarjeta
- Transferencia
- Wallet

De esta manera las implementaciones comparten un contrato común.

⸻

### Polimorfismo

PagoEngine recibe:

metodo_pago: MetodoPago

y utiliza el contrato:
```python
metodo_pago.procesar(total)
```
El motor no necesita conocer la clase concreta utilizada.

Esto permite incorporar nuevas implementaciones sin modificar la lógica principal del motor.

⸻

### Abstracción

Se utilizaron clases abstractas mediante:
```python
ABC
@abstractmethod
```
para establecer contratos comunes para:

* Métodos de pago.
* Estrategias de comisión.
* Observadores de eventos.

⸻

## Patrones de diseño

OrbitPay implementa tres patrones principales.

| Patrón | Implementación | Propósito |
|--------|----------------|-----------|
| Factory | MetodoPagoFactory | Crear métodos de pago |
| Strategy | EstrategiaComision | Intercambiar algoritmos de comisión |
| Observer | GestorEventosPago | Notificar eventos de pago |
### Factory

Permite crear métodos de pago mediante un registro extensible.
```python
MetodoPagoFactory.crear(
    "tarjeta",
    "**** **** **** 1234",
)
```
También permite registrar nuevas implementaciones.

⸻

### Strategy

Permite cambiar la estrategia utilizada para calcular comisiones.

Implementaciones actuales:

ComisionFija
ComisionPorcentual

El motor depende de la abstracción:

EstrategiaComision

y no de una implementación concreta.

⸻

### Observer

Permite notificar eventos generados durante el procesamiento de pagos.

Eventos principales:

PagoAprobado
PagoRechazado

Los observadores pueden reaccionar a estos eventos sin acoplar su implementación al motor.

⸻

## Principios SOLID

La arquitectura incorpora los principios SOLID de la siguiente manera.

### SRP — Single Responsibility Principle

Las responsabilidades principales están separadas:

* Las entidades administran su estado.
* Las estrategias calculan comisiones.
* La Factory crea métodos de pago.
* El gestor administra eventos.
* El Engine coordina el procesamiento.

⸻

### OCP — Open/Closed Principle

La Factory permite registrar nuevos métodos de pago sin modificar su algoritmo principal.

Las estrategias de comisión también pueden extenderse mediante nuevas implementaciones de EstrategiaComision.

⸻

### LSP — Liskov Substitution Principle

Las implementaciones concretas de MetodoPago pueden utilizarse donde se espera un MetodoPago.

El motor trabaja contra la abstracción y no depende de una clase concreta.

⸻

### ISP — Interface Segregation Principle

Los contratos utilizados son pequeños y específicos.

Por ejemplo:
```python
class MetodoPago(ABC):
    @abstractmethod
    def procesar(self, monto: float) -> bool: ...
```
La interfaz únicamente expone la operación necesaria para procesar un pago.

⸻

### DIP — Dependency Inversion Principle

PagoEngine depende de abstracciones:

MetodoPago
EstrategiaComision
GestorEventosPago

en lugar de acoplarse directamente a implementaciones concretas.

⸻

## Idempotencia

El motor mantiene un registro de las transacciones procesadas:

_transacciones_procesadas

Antes de procesar una transacción verifica si ya fue registrada.

Si una transacción intenta procesarse nuevamente, el sistema genera una excepción:

La transacción ... ya fue procesada.

Esto evita realizar accidentalmente dos cargos sobre la misma transacción.

⸻

## Validación y manejo de errores

El dominio incorpora excepciones específicas:
```text
OrbitPayError
├── ValidationError
└── InsufficientBalanceError
```
Esto permite diferenciar errores de validación de situaciones relacionadas con el saldo de una cuenta.

Se validan, entre otros:

* Identificadores vacíos.
* Titulares vacíos.
* Montos menores o iguales a cero.
* Saldos iniciales negativos.
* Estados inválidos.
* Comisiones inválidas.
* Tipos de métodos de pago no registrados.
* Saldo insuficiente.
* Transacciones procesadas previamente.

⸻

## Testing

Las pruebas se encuentran organizadas en:
```text
tests/
├── unit/
└── integration/
```
Las pruebas unitarias verifican componentes individuales y las pruebas de integración validan el comportamiento conjunto del motor de pagos.

La suite cubre los escenarios funcionales principales y casos límite definidos durante el desarrollo.

La cobertura mínima requerida para el proyecto es:

≥ 90 %

La cobertura final será verificada como parte del proceso de publicación.

⸻

## Herramientas de calidad

El proyecto utiliza las siguientes herramientas:

### Black

Formateo automático del código.
```bash
python -m black --check .
```
### Ruff

Análisis estático y detección de problemas de estilo.
```bash
python -m ruff check .
```
### mypy

Verificación estática de tipos.
```bash
python -m mypy --strict orbitpay/
```
### pytest

Ejecución de pruebas automatizadas.
```bash
python -m pytest
```
Estas herramientas forman parte de la estrategia de calidad del proyecto.

⸻

## Refactorización

Se identificaron y corrigieron tres code smells principales.

### Code Smell 1

Problema: modificación directa del estado de Transaccion.

Solución: encapsulamiento mediante _estado, @property, aprobar() y rechazar().

⸻

### Code Smell 2

Problema: Factory con extensibilidad limitada.

Solución: registro dinámico mediante:

MetodoPagoFactory.registrar()

⸻

### Code Smell 3

Problema: duplicación de lógica en los caminos de rechazo de PagoEngine.

Solución: extracción del método:

_rechazar_pago()

⸻

## Evidencia de calidad

Antes de la entrega final se deberá ejecutar:
```bash
python -m black --check .
python -m ruff check .
python -m mypy --strict orbitpay/
python -m pytest
```
Además, se deberá generar el reporte de cobertura:
```bash
python -m pytest \
    --cov=orbitpay \
    --cov-report=term-missing \
    --cov-report=html
```
El objetivo es comprobar que la cobertura de las áreas relevantes del proyecto sea igual o superior al mínimo establecido por la rúbrica.

⸻

## Empaquetado

El proyecto debe poder instalarse como paquete Python.

El proceso de construcción será:
```bash
python -m build
```
Esto deberá generar:
```text
dist/
├── orbitpay-1.0.0-py3-none-any.whl
└── orbitpay-1.0.0.tar.gz
```
La instalación deberá poder realizarse mediante:
```bash
pip install .
```
Y las pruebas deberán poder ejecutarse después de la instalación:
```bash
python -m pytest
```
⸻

## Integración continua

El proyecto contará con un workflow de GitHub Actions para ejecutar automáticamente las verificaciones de calidad.

El pipeline deberá comprobar:

1. Instalación de dependencias.
2. Black.
3. Ruff.
4. mypy.
5. pytest.
6. Cobertura.

El objetivo es evitar que una modificación sea integrada al repositorio si rompe las pruebas o las reglas de calidad establecidas.

⸻

## Documentación generada

Durante el proyecto se desarrollaron los documentos correspondientes a las diferentes fases:
```text
docs/
├── 00-fundamentos.md
├── 01-modelado.md
├── 02-riesgos.md
├── 03-encapsulamiento.md
├── 04-herencia-polimorfismo.md
├── 05-solid-patrones.md
├── 06-testing-refactor.md
└── 07-cierre.md
```
Estos documentos proporcionan trazabilidad entre las competencias estudiadas y la implementación realizada en el repositorio.

⸻

## Entregables finales

Antes de considerar terminada la entrega se deberán completar los siguientes elementos:

* Código fuente.
* README profesional.
* Diagrama UML en SVG.
* LICENSE.
* pyproject.toml.
* Workflow de GitHub Actions.
* Suite de pruebas.
* Reporte de cobertura ≥ 80 %.
* Paquete .whl.
* Paquete .tar.gz.
* Versión 1.0.0.
* Resumen ejecutivo en PDF.
* Preparación de defensa oral.
* Revisión final del repositorio.

⸻

## Criterios de finalización

OrbitPay podrá considerarse listo para entrega cuando:

1. Las pruebas automatizadas sean exitosas.
2. Black no reporte cambios pendientes.
3. Ruff no reporte errores.
4. mypy en modo --strict sea exitoso.
5. La cobertura cumpla el mínimo establecido.
6. El paquete pueda construirse correctamente.
7. El paquete pueda instalarse correctamente.
8. GitHub Actions se encuentre en estado exitoso.
9. La documentación de las fases esté completa.
10. El UML represente la arquitectura implementada.
11. El README permita instalar y ejecutar el proyecto.
12. Los entregables académicos estén preparados.

⸻

## Conclusión

El desarrollo de OrbitPay OO permitió integrar los conceptos de programación orientada a objetos, diseño de software, patrones, principios SOLID, testing y refactorización dentro de un único proyecto.

La evolución del sistema se realizó mediante ciclos de la Metodología Espiral, incorporando identificación de riesgos, construcción incremental, validación y mejora continua.

El proyecto queda preparado para la etapa final de verificación, empaquetado y publicación de la versión 1.0.0.