from orbitpay.domain import Transaccion
from orbitpay.patterns import (
    EventoPago,
    GestorEventosPago,
    ObservadorPago,
    PagoAprobado,
    PagoRechazado,
    RegistroPagosObserver,
)


def crear_transaccion() -> Transaccion:
    return Transaccion(
        id="TRX-001",
        cuenta_id="CTA-001",
        monto=500.0,
    )


def test_pago_aprobado_es_evento_pago() -> None:
    evento = PagoAprobado(
        transaccion=crear_transaccion(),
        mensaje="Pago aprobado",
    )

    assert isinstance(evento, EventoPago)
    assert evento.mensaje == "Pago aprobado"


def test_pago_rechazado_es_evento_pago() -> None:
    evento = PagoRechazado(
        transaccion=crear_transaccion(),
        mensaje="Pago rechazado",
    )

    assert isinstance(evento, EventoPago)
    assert evento.mensaje == "Pago rechazado"


def test_observador_es_abstracto() -> None:
    assert ObservadorPago.__abstractmethods__ == {"actualizar"}


def test_gestor_notifica_observador() -> None:
    gestor = GestorEventosPago()
    observador = RegistroPagosObserver()

    evento = PagoAprobado(
        transaccion=crear_transaccion(),
        mensaje="Pago aprobado",
    )

    gestor.suscribir(observador)
    gestor.notificar(evento)

    assert observador.eventos == [evento]


def test_gestor_notifica_a_multiples_observadores() -> None:
    gestor = GestorEventosPago()
    observador_uno = RegistroPagosObserver()
    observador_dos = RegistroPagosObserver()

    evento = PagoRechazado(
        transaccion=crear_transaccion(),
        mensaje="Saldo insuficiente",
    )

    gestor.suscribir(observador_uno)
    gestor.suscribir(observador_dos)

    gestor.notificar(evento)

    assert observador_uno.eventos == [evento]
    assert observador_dos.eventos == [evento]


def test_gestor_no_duplica_observador() -> None:
    gestor = GestorEventosPago()
    observador = RegistroPagosObserver()

    gestor.suscribir(observador)
    gestor.suscribir(observador)

    evento = PagoAprobado(
        transaccion=crear_transaccion(),
        mensaje="Pago aprobado",
    )

    gestor.notificar(evento)

    assert observador.eventos == [evento]


def test_gestor_puede_eliminar_observador() -> None:
    gestor = GestorEventosPago()
    observador = RegistroPagosObserver()

    gestor.suscribir(observador)
    gestor.eliminar(observador)

    evento = PagoAprobado(
        transaccion=crear_transaccion(),
        mensaje="Pago aprobado",
    )

    gestor.notificar(evento)

    assert observador.eventos == []
