from __future__ import annotations

from abc import ABC, abstractmethod


class MetodoPago(ABC):
    """Define el contrato común para los métodos de pago."""

    @abstractmethod
    def procesar(self, monto: float) -> bool:
        """Procesa un pago y devuelve si fue aprobado."""
        raise NotImplementedError
