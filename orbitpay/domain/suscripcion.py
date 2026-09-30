from __future__ import annotations

from dataclasses import dataclass

from .exceptions import ValidationError


@dataclass
class Suscripcion:
    """Representa una suscripción recurrente."""

    id: str
    cuenta_id: str
    monto_recurrente: float
    activa: bool = True

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValidationError("El identificador de la suscripción es obligatorio.")

        if not self.cuenta_id.strip():
            raise ValidationError("La suscripción debe estar asociada a una cuenta.")

        if self.monto_recurrente <= 0:
            raise ValidationError("El monto recurrente debe ser mayor que cero.")

    def cancelar(self) -> None:
        """Cancela la suscripción."""
        self.activa = False

    def reactivar(self) -> None:
        """Reactiva una suscripción cancelada."""
        self.activa = True
