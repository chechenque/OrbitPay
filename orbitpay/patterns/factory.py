from __future__ import annotations

from collections.abc import Callable

from orbitpay.payments import (
    MetodoPago,
    Tarjeta,
    Transferencia,
    Wallet,
)


class MetodoPagoFactory:
    """Crea implementaciones de MetodoPago."""

    @staticmethod
    def crear(tipo: str, identificador: str) -> MetodoPago:
        """Construye un método de pago según su tipo."""
        tipos: dict[str, Callable[[str], MetodoPago]] = {
            "tarjeta": Tarjeta,
            "transferencia": Transferencia,
            "wallet": Wallet,
        }

        try:
            constructor = tipos[tipo.lower()]
        except KeyError as exc:
            raise ValueError(f"Tipo de método de pago no soportado: {tipo}") from exc

        return constructor(identificador)
