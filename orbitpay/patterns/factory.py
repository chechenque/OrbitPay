from __future__ import annotations

from collections.abc import Callable

from orbitpay.payments import (
    MetodoPago,
    Tarjeta,
    Transferencia,
    Wallet,
)


class MetodoPagoFactory:
    """Factory extensible para crear métodos de pago."""

    _tipos: dict[str, Callable[[str], MetodoPago]] = {
        "tarjeta": Tarjeta,
        "transferencia": Transferencia,
        "wallet": Wallet,
    }

    @classmethod
    def registrar(
        cls,
        tipo: str,
        constructor: Callable[[str], MetodoPago],
    ) -> None:
        """Registra un nuevo tipo de método de pago."""
        tipo_normalizado = tipo.strip().lower()

        if not tipo_normalizado:
            raise ValueError("El tipo de método de pago es obligatorio.")

        cls._tipos[tipo_normalizado] = constructor

    @classmethod
    def crear(
        cls,
        tipo: str,
        identificador: str,
    ) -> MetodoPago:
        """Construye un método de pago registrado."""
        tipo_normalizado = tipo.strip().lower()

        if not tipo_normalizado:
            raise ValueError("El tipo de método de pago es obligatorio.")

        try:
            constructor = cls._tipos[tipo_normalizado]
        except KeyError as exc:
            raise ValueError(f"Tipo de método de pago no soportado: {tipo}") from exc

        return constructor(identificador)
