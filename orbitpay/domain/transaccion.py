from __future__ import annotations

from dataclasses import dataclass
from functools import total_ordering
from typing import Any

from .exceptions import ValidationError


@total_ordering
@dataclass
class Transaccion:
    """Representa una transacción realizada sobre una cuenta."""

    id: str
    cuenta_id: str
    monto: float
    _estado: str = "PENDIENTE"

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValidationError("El identificador de la transacción es obligatorio.")

        if not self.cuenta_id.strip():
            raise ValidationError("La transacción debe estar asociada a una cuenta.")

        if self.monto <= 0:
            raise ValidationError("El monto de la transacción debe ser mayor que cero.")

        estados_validos = {
            "PENDIENTE",
            "APROBADA",
            "RECHAZADA",
        }

        if self._estado not in estados_validos:
            raise ValidationError(f"Estado inválido: {self._estado}")

    @property
    def estado(self) -> str:
        """Devuelve el estado actual de la transacción."""
        return self._estado

    def aprobar(self) -> None:
        """Marca la transacción como aprobada."""
        self._estado = "APROBADA"

    def rechazar(self) -> None:
        """Marca la transacción como rechazada."""
        self._estado = "RECHAZADA"

    def __repr__(self) -> str:
        return (
            f"Transaccion(id={self.id!r}, "
            f"cuenta_id={self.cuenta_id!r}, "
            f"monto={self.monto:.2f}, "
            f"estado={self.estado!r})"
        )

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Transaccion):
            return NotImplemented

        return self.monto < other.monto
