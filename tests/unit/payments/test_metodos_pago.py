import pytest

from orbitpay.payments import (
    MetodoPago,
    Tarjeta,
    Transferencia,
    Wallet,
)


@pytest.mark.parametrize(
    "metodo",
    [
        Tarjeta("**** **** **** 1234"),
        Transferencia("0123456789"),
        Wallet("OrbitWallet"),
    ],
)
def test_metodos_rechazan_montos_invalidos(metodo: MetodoPago) -> None:

    assert metodo.procesar(0.0) is False

    assert metodo.procesar(-100.0) is False


def test_metodo_pago_es_abstracto() -> None:
    assert MetodoPago.__abstractmethods__ == {"procesar"}


def test_tarjeta_implementa_metodo_pago() -> None:
    tarjeta = Tarjeta("**** **** **** 1234")

    assert isinstance(tarjeta, MetodoPago)
    assert tarjeta.procesar(500.0) is True


def test_transferencia_implementa_metodo_pago() -> None:
    transferencia = Transferencia("0123456789")

    assert isinstance(transferencia, MetodoPago)
    assert transferencia.procesar(500.0) is True


def test_wallet_implementa_metodo_pago() -> None:
    wallet = Wallet("OrbitWallet")

    assert isinstance(wallet, MetodoPago)
    assert wallet.procesar(500.0) is True


def test_los_metodos_de_pago_comparten_la_misma_interfaz() -> None:
    metodos: list[MetodoPago] = [
        Tarjeta("**** **** **** 1234"),
        Transferencia("0123456789"),
        Wallet("OrbitWallet"),
    ]

    resultados = [metodo.procesar(100.0) for metodo in metodos]

    assert resultados == [True, True, True]
