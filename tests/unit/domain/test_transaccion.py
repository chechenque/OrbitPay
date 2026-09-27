import pytest

from orbitpay.domain import Transaccion, ValidationError


def test_transaccion_se_crea_correctamente() -> None:
    transaccion = Transaccion(
        id="TRX-001",
        cuenta_id="CTA-001",
        monto=500.0,
    )

    assert transaccion.id == "TRX-001"
    assert transaccion.cuenta_id == "CTA-001"
    assert transaccion.monto == 500.0
    assert transaccion.estado == "PENDIENTE"


def test_transaccion_rechaza_monto_cero() -> None:
    with pytest.raises(ValidationError):
        Transaccion(
            id="TRX-002",
            cuenta_id="CTA-001",
            monto=0.0,
        )


def test_transaccion_rechaza_monto_negativo() -> None:
    with pytest.raises(ValidationError):
        Transaccion(
            id="TRX-003",
            cuenta_id="CTA-001",
            monto=-100.0,
        )


def test_transaccion_rechaza_id_vacio() -> None:
    with pytest.raises(ValidationError):
        Transaccion(
            id="",
            cuenta_id="CTA-001",
            monto=100.0,
        )


def test_transaccion_rechaza_cuenta_vacia() -> None:
    with pytest.raises(ValidationError):
        Transaccion(
            id="TRX-004",
            cuenta_id="",
            monto=100.0,
        )


def test_transacciones_se_comparan_por_monto() -> None:
    menor = Transaccion("TRX-005", "CTA-001", 100.0)
    mayor = Transaccion("TRX-006", "CTA-001", 500.0)

    assert menor < mayor
    assert mayor > menor


def test_transaccion_puede_aprobarse() -> None:
    transaccion = Transaccion(
        id="TRX-009",
        cuenta_id="CTA-001",
        monto=100.0,
    )

    transaccion.aprobar()

    assert transaccion.estado == "APROBADA"


def test_transaccion_puede_rechazarse() -> None:
    transaccion = Transaccion(
        id="TRX-010",
        cuenta_id="CTA-001",
        monto=100.0,
    )

    transaccion.rechazar()

    assert transaccion.estado == "RECHAZADA"


def test_transaccion_rechaza_estado_invalido() -> None:
    with pytest.raises(
        ValidationError,
        match="Estado inválido",
    ):
        Transaccion(
            id="TRX-011",
            cuenta_id="CTA-001",
            monto=100.0,
            _estado="INEXISTENTE",
        )
