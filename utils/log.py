import logging
import logging.handlers
import sys
import threading

from utils.paths import app_path

LOG_FILENAME = "sprite_gibber.log"

log = logging.getLogger("gibber")


def log_path():
    return app_path(LOG_FILENAME)


def setup_logging() -> None:
    """Log to sprite_gibber.log next to the exe/project, and catch every uncaught error.

    In the windowed exe sys.stdout/sys.stderr are None, so stray prints and
    tracebacks would vanish; they are redirected into the log instead.
    """
    if log.handlers:
        return
    log.setLevel(logging.INFO)
    try:
        handler = logging.handlers.RotatingFileHandler(
            log_path(), maxBytes=1_000_000, backupCount=1, encoding="utf-8")
    except OSError:
        handler = logging.NullHandler()  # read-only install dir: keep running without a log
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    log.addHandler(handler)

    if sys.stdout is None or sys.stderr is None:
        stream = _LogStream()
        sys.stdout = sys.stdout or stream
        sys.stderr = sys.stderr or stream

    sys.excepthook = lambda t, v, tb: log.error("Uncaught error", exc_info=(t, v, tb))
    threading.excepthook = lambda a: log.error(
        "Uncaught error in thread %s", a.thread.name if a.thread else "?",
        exc_info=(a.exc_type, a.exc_value, a.exc_traceback))


_FRIENDLY_REASONS = {
    "UnidentifiedImageError": "not a readable image file (corrupt, or not really a PNG)",
    "FileNotFoundError": "file not found (moved or deleted?)",
    "PermissionError": "permission denied (file open in another program, or a read-only folder?)",
    "MemoryError": "out of memory (image or frame count too large?)",
    "DecompressionBombError": "image is far too large to process",
}


def short_reason(exc: BaseException) -> str:
    """One-line, user-facing description of an exception (full details go to the log)."""
    name = type(exc).__name__
    if name in _FRIENDLY_REASONS:
        return _FRIENDLY_REASONS[name]
    msg = str(exc).strip().splitlines()[0] if str(exc).strip() else ""
    return f"{name}: {msg}" if msg else name


class _LogStream:
    def write(self, text):
        text = text.rstrip()
        if text:
            log.info(text)

    def flush(self):
        pass
