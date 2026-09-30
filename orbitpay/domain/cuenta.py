from __future__ import annotations

from dataclasses import dataclass

from .exceptions import InsufficientBalanceError, ValidationError


@dataclass
class Cuenta:
    """Representa una cuenta de OrbitPay."""

    id: str
    titular: str
    _saldo: float = 0.0

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValidationError("El identificador de la cuenta es obligatorio.")

        if not self.titular.strip():
            raise ValidationError("El titular de la cuenta es obligatorio.")

        if self._saldo < 0:
            raise ValidationError("El saldo inicial no puede ser negativo.")

    @property
    def saldo(self) -> float:
        """Devuelve el saldo actual de la cuenta."""
        return self._saldo

    def depositar(self, monto: float) -> None:
        """Incrementa el saldo de la cuenta."""
        self._validar_monto(monto)
        self._saldo += monto

    def retirar(self, monto: float) -> None:
        """Reduce el saldo si existe disponibilidad suficiente."""
        self._validar_monto(monto)

        if monto > self._saldo:
            raise InsufficientBalanceError(
                f"Saldo insuficiente. Disponible: {self._saldo:.2f}"
            )

        self._saldo -= monto

    @staticmethod
    def _validar_monto(monto: float) -> None:
        if monto <= 0:
            raise ValidationError("El monto debe ser mayor que cero.")
