import os

from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        self.base_url = os.getenv("BASE_URL", "https://www.saucedemo.com")
        self.browser = os.getenv("BROWSER", "chromium")
        self.channel = os.getenv("BROWSER_CHANNEL", "").strip() or None
        headless = os.getenv("HEADLESS", "false")
        self.headless = headless.strip().lower() in {"1", "true", "yes", "on"}
        self.slow_mo = int(os.getenv("SLOW_MO", "0"))
        self.default_timeout = int(os.getenv("DEFAULT_TIMEOUT", "10000"))