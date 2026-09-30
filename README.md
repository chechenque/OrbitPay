# OrbitPay OO

Motor de pagos y suscripciones desarrollado en Python aplicando Programación Orientada a Objetos, patrones de diseño, principios SOLID y pruebas automatizadas.

## ¿Qué es OrbitPay?

OrbitPay OO es un motor de procesamiento de pagos y suscripciones para un escenario ficticio de servicios financieros en Latinoamérica.

El proyecto fue desarrollado como un ejercicio integrador de Programación Orientada a Objetos, aplicando una arquitectura modular y extensible para resolver problemas presentes en un sistema monolítico inicial, como:

* Condicionales anidados para seleccionar métodos de pago.
* Duplicación de lógica.
* Riesgo de dobles cargos.
* Modificación directa del estado de las entidades.
* Falta de pruebas automatizadas.
* Alto acoplamiento entre componentes.

El desarrollo se realizó mediante la Metodología Espiral, incorporando análisis de riesgos, prototipos, implementación, pruebas, refactorización y evaluación incremental.

⸻

## Objetivos

El proyecto busca demostrar la aplicación práctica de:

* Encapsulamiento.
* Herencia y polimorfismo.
* Clases abstractas.
* Composición y separación de responsabilidades.
* Principios SOLID.
* Patrones de diseño.
* Validación del dominio.
* Manejo de excepciones.
* Idempotencia.
* Pruebas unitarias e integración.
* Análisis estático y formateo.
* Empaquetado e instalación reproducible.
* Integración continua.

⸻

## Arquitectura

La solución está organizada en cuatro áreas principales:

                         ┌──────────────────────┐
                         │      PagoEngine      │
                         │   Orquestador OO     │
                         └──────────┬───────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
       ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
       │   Domain    │      │  Payments   │      │  Patterns   │
       ├─────────────┤      ├─────────────┤      ├─────────────┤
       │ Cuenta      │      │ MetodoPago  │      │ Factory     │
       │ Transaccion │      │ Tarjeta     │      │ Strategy    │
       │ Suscripcion │      │ Transfer.   │      │ Observer    │
       │ Exceptions  │      │ Wallet      │      │             │
       └─────────────┘      └─────────────┘      └─────────────┘

### Capas principales

#### Domain

Contiene las entidades y reglas fundamentales del negocio:

* Cuenta
* Transaccion
* Suscripcion
* Excepciones del dominio

#### Payments

Define el contrato abstracto MetodoPago y sus implementaciones:

* Tarjeta
* Transferencia
* Wallet

#### Patterns

Contiene los patrones utilizados por el sistema:

* MetodoPagoFactory
* EstrategiaComision
* ComisionFija
* ComisionPorcentual
* GestorEventosPago
* ObservadorPago
* PagoAprobado
* PagoRechazado

#### Engine

PagoEngine coordina el procesamiento de una transacción utilizando las abstracciones anteriores.

⸻

## Patrones de diseño

| Patrón | Implementación | Propósito |
|--------|----------------|-----------|
| Factory | MetodoPagoFactory | Crear métodos de pago sin acoplar al motor a clases concretas |
| Strategy | EstrategiaComision | Permitir diferentes algoritmos de cálculo de comisión |
| Observer | GestorEventosPago | Notificar eventos de pago a diferentes observadores |

### Factory

Permite crear métodos de pago mediante un registro extensible:

```python
metodo = MetodoPagoFactory.crear(
    "tarjeta",
    "**** **** **** 1234",
)
```
El registro puede extenderse sin modificar el motor:
```python
MetodoPagoFactory.registrar(
    "nuevo_metodo",
    ConstructorNuevoMetodo,
)
```
### Strategy

El cálculo de comisión se desacopla del motor:
```
ComisionFija(10.0)
```
o:
```
ComisionPorcentual(2.5)
```
El PagoEngine depende de EstrategiaComision, no de una implementación específica.

### Observer

Los eventos generados durante el procesamiento pueden notificarse a múltiples observadores:
```text
PagoEngine
    │
    ▼
GestorEventosPago
    ├── Observador 1
    ├── Observador 2
    └── Observador N
```
⸻

## Principios SOLID

El diseño aplica los principios SOLID de la siguiente manera:

| Principio | Aplicación |
|-----------|------------|
| SRP | Las entidades, métodos de pago, estrategias, eventos y motor tienen responsabilidades diferenciadas |
| OCP | Factory, Strategy y Observer permiten extender comportamiento sin modificar el núcleo |
| LSP | Tarjeta, Transferencia y Wallet implementan el contrato MetodoPago |
| ISP | Los contratos se mantienen pequeños y específicos |
| DIP | PagoEngine depende de abstracciones como MetodoPago y EstrategiaComision |

⸻

## Reglas importantes del dominio

El sistema implementa reglas para proteger el estado del dominio:

* Una cuenta no puede comenzar con saldo negativo.
* Los depósitos deben tener un monto mayor que cero.
* Los retiros deben tener un monto mayor que cero.
* Una cuenta no puede retirar más dinero del saldo disponible.
* Una transacción requiere identificador y cuenta asociada.
* Una transacción requiere un monto positivo.
* Una transacción solo puede finalizar como aprobada o rechazada.
* Una transacción procesada no puede procesarse nuevamente.
* Las estrategias de comisión validan sus parámetros.

### Idempotencia

El motor mantiene un registro de las transacciones procesadas para evitar procesamientos duplicados:
```text
Transacción nueva
       │
       ▼
¿Ya fue procesada?
   │           │
  Sí           No
   │           │
   ▼           ▼
 Error      Procesamiento
```
Esto evita que una misma transacción sea procesada dos veces por el motor.

⸻

## Tecnologías

* Python 3.11+
* dataclasses
* abc
* pytest
* pytest-cov
* mypy
* ruff
* black
* pre-commit
* setuptools
* build

⸻

## Instalación

1. Clonar el repositorio
```bash
git clone https://github.com/chechenque/OrbitPay.git
cd OrbitPay
```
2. Crear entorno virtual
```bash
python3 -m venv .venv
source .venv/bin/activate
```
En Windows:
```bash
.venv\Scripts\activate
```
3. Instalar dependencias de desarrollo
```bash
python -m pip install -e ".[dev]"
```
⸻

Ejecutar pruebas
```bash
python -m pytest
```
Para ejecutar las pruebas con cobertura:
```bash
python -m pytest --cov=orbitpay --cov-report=term-missing
```
La cobertura obtenida durante la etapa de cierre fue de 98% sobre el paquete orbitpay.

⸻

## Calidad del código

El proyecto utiliza herramientas automatizadas para verificar formato, estilo y tipado.

### Black
```bash
python -m black --check .
```
### Ruff
```bash
python -m ruff check .
```
### Mypy
```bash
python -m mypy --strict orbitpay/
```
### Pruebas
```bash
python -m pytest
```
⸻

## Estructura del proyecto
```text
OrbitPay/
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
│   ├── 00-fundamentos.md
│   ├── 01-modelado.md
│   ├── 02-riesgos.md
│   ├── 03-encapsulamiento.md
│   ├── 04-herencia-polimorfismo.md
│   ├── 05-solid-patrones.md
│   ├── 06-testing-refactor.md
│   ├── 07-cierre.md
│   ├── 08-self-review.md
│   └── class-diagram.svg
├── orbitpay/
│   ├── domain/
│   ├── payments/
│   ├── patterns/
│   └── engine.py
├── spikes/
├── tests/
│   ├── unit/
│   └── integration/
├── .gitignore
├── LICENSE
├── pyproject.toml
└── README.md
```
⸻

## Evidencias de aprendizaje

La documentación del proyecto se organiza de acuerdo con las etapas de la metodología y las competencias trabajadas:

| Documento | Contenido |
|-----------|-----------|
| 00-fundamentos.md | Fundamentos y planificación espiral |
| 01-modelado.md | Modelado orientado a objetos |
| 02-riesgos.md | Identificación y tratamiento de riesgos |
| 03-encapsulamiento.md | Encapsulamiento y protección del estado |
| 04-herencia-polimorfismo.md | Herencia, abstracción y polimorfismo |
| 05-solid-patrones.md | SOLID y patrones de diseño |
| 06-testing-refactor.md | Pruebas y refactorización |
| 07-cierre.md | Cierre técnico del proyecto |
| 08-self-review.md | Autoevaluación y criterios de entrega |

⸻

## Refactorizaciones realizadas

Durante el desarrollo se identificaron y corrigieron tres problemas de diseño:

1. Mutación directa del estado de una transacción

Se encapsuló el estado mediante:
```python
@property
def estado(self) -> str: ...
```
y operaciones explícitas:
```python
transaccion.aprobar()
transaccion.rechazar()
```
2. Factory rígida

La selección basada en condicionales fue reemplazada por un registro extensible de constructores.

3. Duplicación en el rechazo de pagos

La lógica de rechazo fue centralizada en:
```python
_rechazar_pago(...)
```
Esto redujo duplicación y mantuvo una única ruta para actualizar el estado, generar el evento y construir el resultado.

⸻

## Pruebas

El proyecto incluye:

* Pruebas unitarias del dominio.
* Pruebas unitarias de métodos de pago.
* Pruebas de Factory.
* Pruebas de Strategy.
* Pruebas de Observer.
* Pruebas de integración del PagoEngine.
* Casos de saldo insuficiente.
* Casos de montos inválidos.
* Casos de transacciones duplicadas.
* Casos de métodos de pago rechazados.

Cobertura registrada durante la revisión:

255 statements
5 statements sin cubrir
98% cobertura total

⸻

## Estado del proyecto

Fase: Cierre y preparación de release 1.0.0.

Los componentes principales del motor y las pruebas automatizadas se encuentran implementados. Los artefactos de entrega restantes se completan durante la etapa final del proyecto.

⸻

## Roadmap

v1.0.0

* Motor de pagos OO.
* Factory.
* Strategy.
* Observer.
* Validación del dominio.
* Idempotencia.
* Pruebas automatizadas.
* Cobertura ≥80%.
* Análisis estático.
* CI.
* Documentación.
* Empaquetado.

### Evolución futura

* Persistencia de transacciones.
* Integración con proveedores reales de pago.
* Sistema de auditoría.
* Persistencia de suscripciones.
* API externa.
* Observadores para correo y contabilidad.
* Métricas de procesamiento.

Estas funcionalidades quedan fuera del alcance de la versión académica actual.

⸻

## Licencia

Este proyecto se distribuye bajo la licencia MIT.

Consulta el archivo LICENSE para conocer los términos completos.

⸻

## Autor

Luis Angel Leyva Castillo
```text
Proyecto académico — OrbitPay OO
Programación Orientada a Objetos
```