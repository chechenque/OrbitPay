from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from orbitpay.domain import Transaccion


@dataclass(frozen=True)
class EventoPago:
    """Evento base generado durante un pago."""

    transaccion: Transaccion
    mensaje: str


@dataclass(frozen=True)
class PagoAprobado(EventoPago):
    """Evento generado cuando un pago es aprobado."""


@dataclass(frozen=True)
class PagoRechazado(EventoPago):
    """Evento generado cuando un pago es rechazado."""


class ObservadorPago(ABC):
    """Define el contrato para observar eventos de pago."""

    @abstractmethod
    def actualizar(self, evento: EventoPago) -> None:
        """Recibe una notificación de evento de pago."""
        raise NotImplementedError


class GestorEventosPago:
    """Subject encargado de administrar observadores de pagos."""

    def __init__(self) -> None:
        self._observadores: list[ObservadorPago] = []

    def suscribir(self, observador: ObservadorPago) -> None:
        """Registra un nuevo observador."""
        if observador not in self._observadores:
            self._observadores.append(observador)

    def eliminar(self, observador: ObservadorPago) -> None:
        """Elimina un observador registrado."""
        if observador in self._observadores:
            self._observadores.remove(observador)

    def notificar(self, evento: EventoPago) -> None:
        """Notifica el evento a todos los observadores."""
        for observador in self._observadores:
            observador.actualizar(evento)


class RegistroPagosObserver(ObservadorPago):
    """Observador que conserva los eventos recibidos."""

    def __init__(self) -> None:
        self.eventos: list[EventoPago] = []

    def actualizar(self, evento: EventoPago) -> None:
        self.eventos.append(evento)
