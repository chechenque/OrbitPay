from __future__ import annotations

from dataclasses import dataclass

from .metodo_pago import MetodoPago


@dataclass
class Tarjeta(MetodoPago):
    """Método de pago mediante tarjeta."""

    numero_enmascarado: str

    def procesar(self, monto: float) -> bool:
        return monto > 0
