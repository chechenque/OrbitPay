from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from orbitpay.domain import ValidationError


class EstrategiaComision(ABC):
    """Define el contrato para calcular comisiones."""

    @abstractmethod
    def calcular(self, monto: float) -> float:
        """Calcula la comisión correspondiente a un monto."""
        raise NotImplementedError


@dataclass(frozen=True)
class ComisionFija(EstrategiaComision):
    """Aplica una comisión fija por operación."""

    monto_fijo: float

    def __post_init__(self) -> None:
        if self.monto_fijo < 0:
            raise ValidationError("La comisión fija no puede ser negativa.")

    def calcular(self, monto: float) -> float:
        if monto <= 0:
            raise ValidationError("El monto debe ser mayor que cero.")

        return self.monto_fijo


@dataclass(frozen=True)
class ComisionPorcentual(EstrategiaComision):
    """Aplica una comisión porcentual sobre el monto."""

    porcentaje: float

    def __post_init__(self) -> None:
        if not 0 <= self.porcentaje <= 100:
            raise ValidationError("El porcentaje debe estar entre 0 y 100.")

    def calcular(self, monto: float) -> float:
        if monto <= 0:
            raise ValidationError("El monto debe ser mayor que cero.")

        return monto * (self.porcentaje / 100)
