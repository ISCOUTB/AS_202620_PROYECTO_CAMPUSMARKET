class DuplicateEmailError(ValueError):
    """El correo ya está registrado."""


class InvalidCredentialsError(ValueError):
    """La identidad no pudo autenticarse."""


class AuthRateLimitError(ValueError):
    """Demasiados intentos de autenticación."""
