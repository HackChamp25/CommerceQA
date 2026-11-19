"""Global CLI values for the current pytest run.

Populated once from conftest (pytest_configure). Any module can read them:

    from config.runtime import get_cli
    version = get_cli("APP_VERSION")
"""

from __future__ import annotations

import os
from typing import Any

# Filled at session start. Do not mutate in tests.
CLI: dict[str, Any] = {}


def get_cli(key: str, default: Any = None) -> Any:
    if key in CLI:
        return CLI[key]
    return os.getenv(key, default)
