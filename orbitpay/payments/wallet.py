from __future__ import annotations

from dataclasses import dataclass

from .metodo_pago import MetodoPago


@dataclass
class Wallet(MetodoPago):
    """Método de pago mediante una wallet."""

    proveedor: str

    def procesar(self, monto: float) -> bool:
        return monto > 0
