import pytest

from orbitpay.domain import Suscripcion, ValidationError


def test_suscripcion_se_crea_activa() -> None:
    suscripcion = Suscripcion(
        id="SUB-001",
        cuenta_id="CTA-001",
        monto_recurrente=299.0,
    )

    assert suscripcion.id == "SUB-001"
    assert suscripcion.cuenta_id == "CTA-001"
    assert suscripcion.monto_recurrente == 299.0
    assert suscripcion.activa is True


def test_cancelar_desactiva_la_suscripcion() -> None:
    suscripcion = Suscripcion(
        id="SUB-002",
        cuenta_id="CTA-001",
        monto_recurrente=199.0,
    )

    suscripcion.cancelar()

    assert suscripcion.activa is False


def test_reactivar_activa_la_suscripcion() -> None:
    suscripcion = Suscripcion(
        id="SUB-003",
        cuenta_id="CTA-001",
        monto_recurrente=199.0,
    )

    suscripcion.cancelar()
    suscripcion.reactivar()

    assert suscripcion.activa is True


def test_suscripcion_rechaza_monto_cero() -> None:
    with pytest.raises(ValidationError):
        Suscripcion(
            id="SUB-004",
            cuenta_id="CTA-001",
            monto_recurrente=0.0,
        )


def test_suscripcion_rechaza_monto_negativo() -> None:
    with pytest.raises(ValidationError):
        Suscripcion(
            id="SUB-005",
            cuenta_id="CTA-001",
            monto_recurrente=-50.0,
        )


def test_suscripcion_rechaza_id_vacio() -> None:
    with pytest.raises(ValidationError):
        Suscripcion(
            id="",
            cuenta_id="CTA-001",
            monto_recurrente=100.0,
        )


def test_suscripcion_rechaza_cuenta_vacia() -> None:
    with pytest.raises(ValidationError):
        Suscripcion(
            id="SUB-006",
            cuenta_id="",
            monto_recurrente=100.0,
        )
