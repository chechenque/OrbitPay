class OrbitPayError(Exception):
    """Excepción base del dominio OrbitPay."""


class ValidationError(OrbitPayError):
    """Se produce cuando un dato del dominio es inválido."""


class InsufficientBalanceError(OrbitPayError):
    """Se produce cuando una cuenta no tiene saldo suficiente."""
