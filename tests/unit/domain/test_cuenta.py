import pytest

from orbitpay.domain import (
    Cuenta,
    InsufficientBalanceError,
    ValidationError,
)


def test_cuenta_se_crea_con_saldo_inicial() -> None:
    cuenta = Cuenta("CTA-001", "Luis Angel", 1000.0)

    assert cuenta.id == "CTA-001"
    assert cuenta.titular == "Luis Angel"
    assert cuenta.saldo == 1000.0


def test_cuenta_inicia_con_saldo_cero() -> None:
    cuenta = Cuenta("CTA-002", "Ana")

    assert cuenta.saldo == 0.0


def test_depositar_incrementa_el_saldo() -> None:
    cuenta = Cuenta("CTA-003", "Carlos", 500.0)

    cuenta.depositar(250.0)

    assert cuenta.saldo == 750.0


def test_retirar_disminuye_el_saldo() -> None:
    cuenta = Cuenta("CTA-004", "Maria", 1000.0)

    cuenta.retirar(300.0)

    assert cuenta.saldo == 700.0


def test_no_permite_retirar_mas_del_saldo() -> None:
    cuenta = Cuenta("CTA-005", "Pedro", 100.0)

    with pytest.raises(InsufficientBalanceError):
        cuenta.retirar(150.0)

    assert cuenta.saldo == 100.0


def test_no_permite_saldo_inicial_negativo() -> None:
    with pytest.raises(ValidationError):
        Cuenta("CTA-006", "Laura", -1.0)


@pytest.mark.parametrize("monto", [0.0, -10.0])
def test_no_permite_depositos_invalidos(monto: float) -> None:
    cuenta = Cuenta("CTA-007", "Sofia")

    with pytest.raises(ValidationError):
        cuenta.depositar(monto)


@pytest.mark.parametrize("monto", [0.0, -10.0])
def test_no_permite_retiros_invalidos(monto: float) -> None:
    cuenta = Cuenta("CTA-008", "Diego", 500.0)

    with pytest.raises(ValidationError):
        cuenta.retirar(monto)


def test_no_permite_id_vacio() -> None:
    with pytest.raises(ValidationError):
        Cuenta("", "Luis Angel")


def test_no_permite_titular_vacio() -> None:
    with pytest.raises(ValidationError):
        Cuenta("CTA-009", "")
