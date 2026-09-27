from __future__ import annotations

from dataclasses import dataclass

from .metodo_pago import MetodoPago


@dataclass
class Transferencia(MetodoPago):
    """Método de pago mediante transferencia bancaria."""

    cuenta_bancaria: str

    def procesar(self, monto: float) -> bool:
        return monto > 0
