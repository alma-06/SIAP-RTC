from __future__ import annotations

from datetime import timedelta
import re

_DURATION_RE = re.compile(r"^(?:(\d+):)?(\d{1,2}):(\d{1,2})(?:\.(\d+))?$")


def duration_to_seconds(value: object) -> int:
    """Convert HH:MM:SS or MM:SS duration to whole seconds.

    Rejects malformed and negative values. Fractional seconds are accepted but
    deliberately truncated because RTC reporting is aggregated at whole-second
    precision in this layer.
    """
    if value is None or value == "":
        raise ValueError("La duración es obligatoria")

    if isinstance(value, timedelta):
        seconds = int(value.total_seconds())
        if seconds < 0:
            raise ValueError("La duración no puede ser negativa")
        return seconds

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if value < 0:
            raise ValueError("La duración no puede ser negativa")
        # Excel may expose a time-only value as a fraction of a day.
        if 0 <= value < 1:
            return int(value * 86400)
        return int(value)

    text = str(value).strip()
    match = _DURATION_RE.fullmatch(text)
    if not match:
        raise ValueError(f"Formato de duración no reconocido: {value!r}")

    hours = int(match.group(1) or 0)
    minutes = int(match.group(2))
    seconds = int(match.group(3))
    if minutes > 59 or seconds > 59:
        raise ValueError(f"Duración inválida: {value!r}")
    return hours * 3600 + minutes * 60 + seconds


def seconds_to_hhmmss(seconds: int) -> str:
    if seconds < 0:
        raise ValueError("Los segundos no pueden ser negativos")
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def seconds_to_excel_elapsed(seconds: int) -> str:
    """Format elapsed time, preserving hours beyond 24 as [h]:mm:ss."""
    if seconds < 0:
        raise ValueError("Los segundos no pueden ser negativos")
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}:{minutes:02d}:{seconds:02d}"
