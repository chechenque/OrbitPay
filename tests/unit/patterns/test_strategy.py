import pytest

from orbitpay.domain import ValidationError
from orbitpay.patterns import (
    ComisionFija,
    ComisionPorcentual,
    EstrategiaComision,
)


def test_comision_fija() -> None:
    estrategia = ComisionFija(25.0)

    assert estrategia.calcular(500.0) == 25.0


def test_comision_porcentual() -> None:
    estrategia = ComisionPorcentual(2.5)

    assert estrategia.calcular(1000.0) == 25.0


def test_strategy_es_abstracta() -> None:
    assert EstrategiaComision.__abstractmethods__ == {"calcular"}


def test_estrategias_comparten_la_misma_interfaz() -> None:
    estrategias: list[EstrategiaComision] = [
        ComisionFija(10.0),
        ComisionPorcentual(2.0),
    ]

    resultados = [estrategia.calcular(500.0) for estrategia in estrategias]

    assert resultados == [10.0, 10.0]


def test_comision_fija_no_puede_ser_negativa() -> None:
    with pytest.raises(
        ValidationError,
        match="no puede ser negativa",
    ):
        ComisionFija(-1.0)


def test_comision_porcentual_debe_estar_en_rango() -> None:
    with pytest.raises(
        ValidationError,
        match="entre 0 y 100",
    ):
        ComisionPorcentual(101.0)


@pytest.mark.parametrize(
    "estrategia",
    [
        ComisionFija(10.0),
        ComisionPorcentual(2.0),
    ],
)
def test_estrategias_rechazan_montos_invalidos(
    estrategia: EstrategiaComision,
) -> None:
    with pytest.raises(
        ValidationError,
        match="mayor que cero",
    ):
        estrategia.calcular(0.0)
