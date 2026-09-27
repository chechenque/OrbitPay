from __future__ import annotations

from dataclasses import dataclass
from functools import total_ordering
from typing import Any

from .exceptions import ValidationError


@total_ordering
@dataclass
class Transaccion:
    """Representa una operación monetaria de OrbitPay."""

    id: str
    cuenta_id: str
    monto: float
    estado: str = "PENDIENTE"

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValidationError("El identificador de la transacción es obligatorio.")

        if not self.cuenta_id.strip():
            raise ValidationError("La transacción debe estar asociada a una cuenta.")

        if self.monto <= 0:
            raise ValidationError("El monto de la transacción debe ser mayor que cero.")

    def __repr__(self) -> str:
        return (
            f"Transaccion(id={self.id!r}, cuenta_id={self.cuenta_id!r}, "
            f"monto={self.monto:.2f}, estado={self.estado!r})"
        )

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Transaccion):
            return NotImplemented

        return self.monto < other.monto
