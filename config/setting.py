import os

from dotenv import load_dotenv

from config.endpoints import VERSION_URLS
from config.runtime import get_cli

load_dotenv()


class Settings:
    def __init__(self, app_version: str | None = None):
        self.app_version = (
            app_version
            or get_cli("APP_VERSION", "v1")
        )
        self.app_version = str(self.app_version).strip().lower()

        if self.app_version not in VERSION_URLS:
            raise ValueError(
                f"Unsupported APP_VERSION '{self.app_version}'. "
                f"Use one of: {', '.join(VERSION_URLS)}"
            )

        version_urls = VERSION_URLS[self.app_version]

        # CLI/env APP_VERSION wins for segregation; env URL overrides stay optional
        self.base_url = os.getenv("BASE_URL", version_urls["ui_base_url"])
        self.api_base_url = os.getenv("API_BASE_URL", version_urls["api_base_url"])

        self.browser = os.getenv("BROWSER", "chromium")
        self.channel = os.getenv("BROWSER_CHANNEL", "").strip() or None
        headless = os.getenv("HEADLESS", "false")
        self.headless = headless.strip().lower() in {"1", "true", "yes", "on"}
        self.slow_mo = int(os.getenv("SLOW_MO", "0"))
        self.default_timeout = int(os.getenv("DEFAULT_TIMEOUT", "10000"))
        self.api_timeout = int(os.getenv("API_TIMEOUT", "15"))
