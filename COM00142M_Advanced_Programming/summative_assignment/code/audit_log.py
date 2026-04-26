"""Central audit / application logging: ``log.txt`` (INFO+) and stderr (ERROR+ only)."""
from __future__ import annotations

import logging
import sys
from pathlib import Path

_LOG = logging.getLogger('app.audit')
_CONFIGURED = False

# Same directory as this package (project root when run from the project folder).
LOG_FILE = Path(__file__).resolve().parent / 'log.txt'


def configure_audit_logging() -> None:
    """Attach file + stderr handlers once (idempotent)."""
    global _CONFIGURED
    if _CONFIGURED:
        return
    _CONFIGURED = True

    _LOG.setLevel(logging.INFO)
    _LOG.handlers.clear()

    fmt = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(fmt)

    err_handler = logging.StreamHandler(sys.stderr)
    err_handler.setLevel(logging.ERROR)
    err_handler.setFormatter(fmt)

    _LOG.addHandler(file_handler)
    _LOG.addHandler(err_handler)
    _LOG.propagate = False


def get_audit_logger() -> logging.Logger:
    """Return the shared audit logger, configuring handlers on first use."""
    configure_audit_logging()
    return _LOG
