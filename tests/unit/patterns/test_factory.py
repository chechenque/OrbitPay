import pytest

from orbitpay.patterns import MetodoPagoFactory
from orbitpay.payments import (
    MetodoPago,
    Tarjeta,
    Transferencia,
    Wallet,
)


def test_factory_crea_tarjeta() -> None:
    metodo = MetodoPagoFactory.crear(
        "tarjeta",
        "**** **** **** 1234",
    )

    assert isinstance(metodo, Tarjeta)
    assert isinstance(metodo, MetodoPago)


def test_factory_crea_transferencia() -> None:
    metodo = MetodoPagoFactory.crear(
        "transferencia",
        "0123456789",
    )

    assert isinstance(metodo, Transferencia)
    assert isinstance(metodo, MetodoPago)


def test_factory_crea_wallet() -> None:
    metodo = MetodoPagoFactory.crear(
        "wallet",
        "OrbitWallet",
    )

    assert isinstance(metodo, Wallet)
    assert isinstance(metodo, MetodoPago)


def test_factory_acepta_mayusculas() -> None:
    metodo = MetodoPagoFactory.crear(
        "TARJETA",
        "**** **** **** 1234",
    )

    assert isinstance(metodo, Tarjeta)


def test_factory_rechaza_tipo_no_soportado() -> None:
    with pytest.raises(ValueError, match="no soportado"):
        MetodoPagoFactory.crear(
            "cheque",
            "12345",
        )
