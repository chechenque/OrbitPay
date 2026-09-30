# OrbitPay OO — Fundamentos de la Espiral y Diseño Orientado a Objetos

## Propósito del documento

Este documento establece los fundamentos metodológicos y de diseño del proyecto OrbitPay OO, un motor de pagos y suscripciones desarrollado en Python mediante programación orientada a objetos.

El proyecto se construirá utilizando la Metodología Espiral, dividiendo el desarrollo en ciclos controlados. En cada vuelta se planificarán objetivos, se identificarán riesgos, se implementará una solución y se evaluarán los resultados antes de continuar con la siguiente iteración.

El propósito es reducir progresivamente el riesgo técnico y construir el sistema de manera incremental, utilizando las pruebas y la documentación como mecanismos de control de calidad.

⸻

## Contexto de OrbitPay

OrbitPay es una procesadora ficticia de pagos y suscripciones que atiende a comercios de Latinoamérica.

El sistema existente presenta problemas derivados de un diseño monolítico:

* La lógica de pagos se encuentra concentrada en funciones grandes.
* Cada nuevo método de pago requiere modificar código existente.
* Existen riesgos de doble cobro.
* Los saldos pueden quedar inconsistentes.
* Las reglas de comisión están acopladas al motor principal.
* Las modificaciones son difíciles de realizar porque no existe una cobertura adecuada de pruebas.

OrbitPay OO busca reconstruir este motor utilizando un diseño orientado a objetos que permita:

* encapsular el estado de las entidades;
* agregar métodos de pago sin modificar el núcleo;
* separar las reglas de comisión;
* notificar eventos sin acoplar los componentes;
* probar cada parte de forma independiente;
* refactorizar el código de forma segura.

⸻
## Objetivo de la primera espiral

La primera espiral tiene como objetivo establecer una base técnica y metodológica sólida para el proyecto.

Al finalizar esta etapa se deberá contar con:

1. Un plan de desarrollo basado en la Metodología Espiral.
2. Una identificación inicial de los riesgos.
3. Un dominio inicial definido.
4. Las principales clases candidatas identificadas.
5. Una estructura inicial del paquete Python.
6. Una estrategia para evolucionar desde un núcleo OO básico hasta un diseño con patrones y pruebas.

⸻

## Metodología Espiral

OrbitPay OO se desarrollará mediante ciclos sucesivos.

Cada vuelta seguirá cuatro actividades principales:
```
┌─────────────────────────────┐
│       PLANIFICACIÓN         │
│ Objetivo y entregables      │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│      ANÁLISIS DE RIESGO     │
│ Riesgos y alternativas      │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│         INGENIERÍA          │
│ Diseño + implementación     │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│        EVALUACIÓN           │
│ Tests + revisión + feedback │
└──────────────┬──────────────┘
               │
               └──────────────► Siguiente vuelta
```

La finalidad de este enfoque es evitar construir todo el sistema de una sola vez. Cada iteración debe producir evidencia que permita tomar mejores decisiones en la siguiente.

⸻

## Vueltas planificadas

El proyecto se dividirá en ocho vueltas principales, correspondientes a las ocho lecciones del módulo.

| Vuelta | Lección | Objetivo | Riesgo principal | Entregable |
|--------|---------|----------|------------------|------------|
| 1 | L1 | Definir metodología y dominio | Diseñar sin una estrategia clara | Fundamentos y estructura inicial |
| 2 | L2 | Levantar requisitos y modelar clases | Modelo incorrecto o responsabilidades ambiguas | Requisitos + UML |
| 3 | L3 | Analizar riesgos y validar arquitectura | Doble cobro, inconsistencias y acoplamiento | Risk register + prototipo |
| 4 | L4 | Implementar núcleo OO | Estado inválido y falta de encapsulamiento | Dominio funcional |
| 5 | L5 | Incorporar herencia y polimorfismo | Acoplamiento a tipos concretos | Jerarquía MetodoPago |
| 6 | L6 | Aplicar SOLID y patrones | Diseño rígido y difícil de extender | Factory + Strategy + Observer |
| 7 | L7 | Probar y refactorizar | Regresiones y code smells | Suite + cobertura + refactors |
| 8 | L8 | Integrar y entregar | Fallos de instalación o integración | Paquete + CI + cierre |

La fase de validación y defensa se realizará posteriormente como una etapa transversal de comprobación de todas las competencias.

⸻
## Criterios de avance entre vueltas

Una vuelta no se considera terminada únicamente porque el código funcione.

Para avanzar a la siguiente vuelta deberán existir:

* el entregable correspondiente;
* documentación de las decisiones importantes;
* evidencia de las pruebas realizadas;
* riesgos relevantes identificados;
* código en un estado funcional;
* criterios de aceptación cumplidos.

La siguiente vuelta podrá modificar decisiones anteriores cuando exista evidencia técnica que lo justifique.

⸻

## Pilares de la Programación Orientada a Objetos

### Abstracción

La abstracción permite representar únicamente los elementos relevantes del dominio y ocultar detalles que no son necesarios para utilizar un objeto.

En OrbitPay, MetodoPago representará el concepto general de un método utilizado para procesar un pago.

El motor no necesita conocer todos los detalles internos de una tarjeta, transferencia o wallet. Solo necesita trabajar con el contrato común definido por la abstracción.

Ejemplo conceptual:
```
MetodoPago
    │
    ├── Tarjeta
    ├── Transferencia
    └── Wallet
```

Esto permitirá que el motor trabaje con diferentes métodos de pago mediante una misma interfaz.

⸻

### Encapsulamiento

El encapsulamiento consiste en proteger el estado interno de los objetos y controlar cómo puede modificarse.

En OrbitPay, valores críticos como el saldo de una cuenta no deberán modificarse directamente desde el exterior.

En lugar de:
```python
cuenta.saldo = -500
```
se utilizarán propiedades y métodos que validen las reglas del dominio.

Por ejemplo:

```python
cuenta.depositar(500)
cuenta.retirar(200)
```

La propia clase será responsable de garantizar que sus invariantes se mantengan.

Una regla fundamental será:

El saldo de una cuenta nunca puede quedar por debajo de cero.

⸻

### Herencia

La herencia permitirá crear especializaciones de una abstracción común.

En OrbitPay, los diferentes métodos de pago compartirán el contrato definido por MetodoPago.
```
MetodoPago
├── Tarjeta
├── Transferencia
└── Wallet
```

Las clases hijas podrán proporcionar implementaciones específicas del procesamiento sin duplicar la estructura común.

⸻

### Polimorfismo

El polimorfismo permitirá que el motor utilice diferentes métodos de pago mediante una misma abstracción.

El objetivo es que el motor pueda recibir:
```python
MetodoPago
```

sin necesitar conocer si el objeto concreto es:

- Tarjeta
- Transferencia
- Wallet

Por lo tanto, el diseño deberá evitar construcciones como:
```python
if tipo == "tarjeta":
    ...
elif tipo == "transferencia":
    ...
elif tipo == "wallet":
    ...
```
También se evitará utilizar isinstance() para resolver decisiones que correspondan al comportamiento polimórfico.

La decisión sobre cómo procesar el pago pertenecerá al objeto especializado.

⸻

8. Dominio inicial de OrbitPay

Durante esta primera vuelta se identifican las siguientes clases candidatas:

| Clase | Responsabilidad inicial |
|-------|-------------------------|
| Cuenta | Mantener la identidad y el saldo de un cliente, protegiendo sus invariantes. |
| Transaccion | Representar una operación de pago y conservar su información y estado. |
| Suscripcion | Representar una relación recurrente de cobro entre un cliente y un servicio. |
| MetodoPago | Definir el contrato común para procesar pagos. |

En las siguientes iteraciones se incorporarán las especializaciones y componentes necesarios.

⸻

## Responsabilidades iniciales

### Cuenta

La clase Cuenta será responsable de administrar el saldo asociado a una cuenta.

Responsabilidades:

* almacenar la identidad de la cuenta;
* mantener el saldo;
* permitir operaciones válidas sobre el saldo;
* impedir estados inválidos;
* validar montos.

No deberá ser responsable de enviar correos, calcular comisiones ni seleccionar métodos de pago.

⸻

### Transaccion

La clase Transaccion representará una operación realizada dentro del sistema.

Responsabilidades:

* identificar la operación;
* almacenar el monto;
* registrar el método de pago utilizado;
* mantener el estado de la operación;
* proporcionar una representación consistente del pago.

La transacción no deberá encargarse de administrar directamente las notificaciones externas.

⸻

### Suscripcion

La clase Suscripcion representará un acuerdo de cobro recurrente.

Responsabilidades:

* identificar la suscripción;
* mantener su estado;
* asociarla con una cuenta;
* representar el monto recurrente;
* controlar las condiciones básicas de la suscripción.

La lógica de procesamiento del método de pago deberá permanecer separada.

⸻

### MetodoPago

MetodoPago será una abstracción para representar las distintas formas de procesar un pago.

Responsabilidades:

* definir el contrato común;
* validar la información necesaria;
* procesar un monto;
* permitir implementaciones especializadas.

Las implementaciones concretas serán desarrolladas en la quinta vuelta.

⸻

## Principios de diseño iniciales

Desde esta primera vuelta se establecen las siguientes reglas:

### Estado crítico encapsulado

Los atributos críticos no serán expuestos como estado mutable público.

Especialmente:

* saldo;
* estado de transacción;
* estado de suscripción.

⸻

### Programación contra abstracciones

Los componentes de alto nivel deberán depender de abstracciones en lugar de implementaciones concretas.

Esto será especialmente importante para MetodoPago.

⸻

### Responsabilidad única

Cada clase deberá tener una responsabilidad claramente delimitada.

Si una clase comienza a administrar pagos, comisiones, notificaciones, persistencia y reportes simultáneamente, deberá revisarse el diseño.

⸻

### Extensibilidad

Agregar un nuevo método de pago no debería requerir modificar el motor principal.

La arquitectura evolucionará hacia este modelo:
```
                 ┌───────────────┐
                 │  PaymentEngine│
                 └───────┬───────┘
                         │
                         ▼
                  ┌────────────┐
                  │ MetodoPago │
                  │    ABC     │
                  └─────┬──────┘
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
      Tarjeta     Transferencia     Wallet
```
⸻

## Estructura inicial del repositorio

La estructura inicial será:
```
orbitpay/
├── README.md
├── LICENSE
├── pyproject.toml
│
├── docs/
│   └── 00-fundamentos.md
│
├── orbitpay/
│   └── __init__.py
│
├── tests/
│
└── spikes/
```
La estructura evolucionará durante las siguientes fases hasta incorporar:
```
orbitpay/
├── domain/
├── payments/
├── patterns/
└── engine.py
```
⸻

## Criterios de éxito de la primera vuelta

La primera vuelta se considera completada cuando:

* Se definió la metodología de desarrollo.
* Se establecieron las vueltas de la espiral.
* Se identificaron los objetivos de cada vuelta.
* Se identificaron las principales clases del dominio.
* Se definieron sus responsabilidades iniciales.
* Se documentaron los cuatro pilares OO aplicados al sistema.
* Se establecieron principios iniciales de diseño.
* Se creó el esqueleto físico del paquete Python.
* import orbitpay funciona correctamente.
* Se incorporó el diagrama de la espiral como evidencia visual.

Los dos últimos puntos serán completados directamente en el repositorio como parte de la implementación de la fase.

⸻

## Próxima vuelta

La segunda vuelta corresponderá a L2 — Planificación: Análisis de Requisitos y Modelado de Clases.

En ella se transformará el dominio inicial en un modelo más preciso mediante:

1. requisitos funcionales;
2. requisitos no funcionales;
3. diagrama UML;
4. responsabilidades detalladas;
5. relaciones entre clases;
6. esqueletos de las clases del dominio.

La decisión de esta primera vuelta será considerada una hipótesis de diseño y podrá refinarse si el modelado o el análisis de riesgos de las siguientes vueltas proporcionan evidencia para modificarla.

⸻

## Conclusión

OrbitPay OO será construido de forma incremental mediante la Metodología Espiral. La primera vuelta establece el marco para que las decisiones posteriores sean verificables y puedan evolucionar sin perder trazabilidad.

El objetivo no es únicamente obtener un programa que procese pagos, sino demostrar un proceso completo de ingeniería orientada a objetos: planificar, identificar riesgos, modelar, implementar, probar, refactorizar, integrar y entregar.

La arquitectura se desarrollará progresivamente, manteniendo como principios fundamentales el encapsulamiento, la abstracción, la responsabilidad única, el polimorfismo y la extensibilidad.