import logging
from pathlib import Path

def configure_logging():
    log_directory = Path("reports/logs")
    log_directory.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(level = logging.INFO,
                        format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                        handlers = [
                            logging.FileHandler(log_directory / "automation.log", mode="w", encoding="utf-8"),
                            logging.StreamHandler()
                        ],force=True)