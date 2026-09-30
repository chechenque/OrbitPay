from __future__ import annotations

from dataclasses import dataclass

from orbitpay.domain import (
    Cuenta,
    InsufficientBalanceError,
    Transaccion,
)
from orbitpay.patterns import (
    EstrategiaComision,
    EventoPago,
    GestorEventosPago,
    PagoAprobado,
    PagoRechazado,
)
from orbitpay.payments import MetodoPago


@dataclass(frozen=True)
class ResultadoPago:
    """Representa el resultado de una operación de pago."""

    transaccion: Transaccion
    aprobado: bool
    comision: float
    total: float


class PagoEngine:
    """Coordina el procesamiento de pagos de OrbitPay."""

    def __init__(
        self,
        estrategia_comision: EstrategiaComision,
        gestor_eventos: GestorEventosPago,
    ) -> None:
        self._estrategia_comision = estrategia_comision
        self._gestor_eventos = gestor_eventos
        self._transacciones_procesadas: set[str] = set()

    def procesar_pago(
        self,
        cuenta: Cuenta,
        metodo_pago: MetodoPago,
        transaccion: Transaccion,
    ) -> ResultadoPago:
        """Procesa un pago de forma segura e idempotente."""

        if transaccion.id in self._transacciones_procesadas:
            raise ValueError(f"La transacción {transaccion.id} ya fue procesada.")

        comision = self._estrategia_comision.calcular(transaccion.monto)
        total = transaccion.monto + comision

        try:
            aprobado = metodo_pago.procesar(total)

            if not aprobado:
                return self._rechazar_pago(
                    transaccion=transaccion,
                    comision=comision,
                    total=total,
                    mensaje="El método de pago rechazó la operación.",
                )

            cuenta.retirar(total)
            transaccion.aprobar()

        except InsufficientBalanceError:
            return self._rechazar_pago(
                transaccion=transaccion,
                comision=comision,
                total=total,
                mensaje="Saldo insuficiente en la cuenta.",
            )

        evento_aprobado = PagoAprobado(
            transaccion=transaccion,
            mensaje="Pago procesado correctamente.",
        )
        self._notificar(evento_aprobado)

        self._transacciones_procesadas.add(transaccion.id)

        return ResultadoPago(
            transaccion=transaccion,
            aprobado=True,
            comision=comision,
            total=total,
        )

    def _rechazar_pago(
        self,
        transaccion: Transaccion,
        comision: float,
        total: float,
        mensaje: str,
    ) -> ResultadoPago:
        """Gestiona de forma centralizada el rechazo de un pago."""
        transaccion.rechazar()

        evento_rechazado = PagoRechazado(
            transaccion=transaccion,
            mensaje=mensaje,
        )
        self._notificar(evento_rechazado)

        self._transacciones_procesadas.add(transaccion.id)

        return ResultadoPago(
            transaccion=transaccion,
            aprobado=False,
            comision=comision,
            total=total,
        )

    def _notificar(self, evento: EventoPago) -> None:
        """Notifica un evento generado por el motor."""
        self._gestor_eventos.notificar(evento)
