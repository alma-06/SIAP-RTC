"""Domain-specific exceptions."""


class DomainError(Exception):
    """Base exception for SIAP-RTC domain violations."""


class ValidationError(DomainError):
    """Raised when imported or constructed data violates domain rules."""
