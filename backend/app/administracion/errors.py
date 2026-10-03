class ReportNotFoundError(LookupError):
    """El reporte no existe."""


class ReportConflictError(ValueError):
    """El reporte ya existe o fue resuelto."""


class InvalidReportError(ValueError):
    """La publicación no se puede reportar."""
