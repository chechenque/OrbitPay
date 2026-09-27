import pytest

from orbitpay.domain import Cuenta, Transaccion
from orbitpay.engine import PagoEngine
from orbitpay.patterns import (
    ComisionFija,
    GestorEventosPago,
    PagoAprobado,
    PagoRechazado,
    RegistroPagosObserver,
)
from orbitpay.payments import Tarjeta


def crear_engine() -> tuple[PagoEngine, RegistroPagosObserver]:
    gestor = GestorEventosPago()
    observador = RegistroPagosObserver()

    gestor.suscribir(observador)

    engine = PagoEngine(
        estrategia_comision=ComisionFija(10.0),
        gestor_eventos=gestor,
    )

    return engine, observador


def test_pago_aprobado_descuenta_monto_mas_comision() -> None:
    engine, observador = crear_engine()

    cuenta = Cuenta(
        id="CTA-001",
        titular="Luis",
        _saldo=1000.0,
    )

    transaccion = Transaccion(
        id="TRX-001",
        cuenta_id=cuenta.id,
        monto=200.0,
    )

    resultado = engine.procesar_pago(
        cuenta=cuenta,
        metodo_pago=Tarjeta("**** **** **** 1234"),
        transaccion=transaccion,
    )

    assert resultado.aprobado is True
    assert resultado.comision == 10.0
    assert resultado.total == 210.0
    assert cuenta.saldo == 790.0
    assert transaccion.estado == "APROBADA"

    assert len(observador.eventos) == 1
    assert isinstance(observador.eventos[0], PagoAprobado)


def test_pago_rechazado_por_saldo_insuficiente() -> None:
    engine, observador = crear_engine()

    cuenta = Cuenta(
        id="CTA-002",
        titular="Luis",
        _saldo=100.0,
    )

    transaccion = Transaccion(
        id="TRX-002",
        cuenta_id=cuenta.id,
        monto=200.0,
    )

    resultado = engine.procesar_pago(
        cuenta=cuenta,
        metodo_pago=Tarjeta("**** **** **** 1234"),
        transaccion=transaccion,
    )

    assert resultado.aprobado is False
    assert cuenta.saldo == 100.0
    assert transaccion.estado == "RECHAZADA"

    assert len(observador.eventos) == 1
    assert isinstance(observador.eventos[0], PagoRechazado)


def test_no_se_puede_procesar_dos_veces_la_misma_transaccion() -> None:
    engine, _ = crear_engine()

    cuenta = Cuenta(
        id="CTA-003",
        titular="Luis",
        _saldo=1000.0,
    )

    transaccion = Transaccion(
        id="TRX-003",
        cuenta_id=cuenta.id,
        monto=100.0,
    )

    engine.procesar_pago(
        cuenta=cuenta,
        metodo_pago=Tarjeta("**** **** **** 1234"),
        transaccion=transaccion,
    )

    saldo_despues_del_primer_pago = cuenta.saldo

    with pytest.raises(ValueError, match="ya fue procesada"):
        engine.procesar_pago(
            cuenta=cuenta,
            metodo_pago=Tarjeta("**** **** **** 1234"),
            transaccion=transaccion,
        )

    assert cuenta.saldo == saldo_despues_del_primer_pago


def test_pago_rechazado_por_metodo_de_pago() -> None:
    engine, observador = crear_engine()

    cuenta = Cuenta(
        id="CTA-004",
        titular="Luis",
        _saldo=1000.0,
    )

    transaccion = Transaccion(
        id="TRX-004",
        cuenta_id=cuenta.id,
        monto=100.0,
    )

    class MetodoRechazado(Tarjeta):
        def procesar(self, monto: float) -> bool:
            return False

    resultado = engine.procesar_pago(
        cuenta=cuenta,
        metodo_pago=MetodoRechazado("**** **** **** 0000"),
        transaccion=transaccion,
    )

    assert resultado.aprobado is False
    assert cuenta.saldo == 1000.0
    assert transaccion.estado == "RECHAZADA"
    assert isinstance(observador.eventos[0], PagoRechazado)
