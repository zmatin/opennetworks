# conftest.py
import os
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

from webdriver_manager.firefox import GeckoDriverManager

from utilities import config

# --- Load local driver paths, but keep them out of git ---
# Try local_paths.py first (ignored by git). If missing, fall back to env vars.
try:
    from utilities import local_paths  # noqa: F401
    LOCAL_CHROME = getattr(local_paths, "CHROMEDRIVER_PATH", None)
    LOCAL_EDGE = getattr(local_paths, "MSEDGEDRIVER_PATH", None)
except Exception:
    LOCAL_CHROME = os.getenv("CHROMEDRIVER_PATH")
    LOCAL_EDGE = os.getenv("MSEDGEDRIVER_PATH")


def _require_existing(path_value: str, name: str) -> str:
    """Validate that a driver path exists; raise a friendly error if not."""
    if not path_value:
        raise RuntimeError(
            f"{name} is not set. Create utilities/local_paths.py with {name} "
            f"or set the {name} environment variable."
        )
    if not os.path.exists(path_value):
        raise RuntimeError(
            f"{name} points to a non-existent file:\n{path_value}\n"
            f"Fix the path in utilities/local_paths.py."
        )
    return path_value


def _build_driver(browser_name: str):
    b = browser_name.lower()

    if b == "firefox":
        # Use WebDriverManager for Firefox (your preference)
        options = FirefoxOptions()
        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)

    if b == "chrome":
        # Use LOCAL chromedriver; do NOT fall back to WDM to avoid mismatches/leaks
        chromedriver_path = _require_existing(LOCAL_CHROME, "CHROMEDRIVER_PATH")
        options = ChromeOptions()
        service = ChromeService(chromedriver_path)
        return webdriver.Chrome(service=service, options=options)

    if b == "edge":
        # Use LOCAL msedgedriver; do NOT fall back to WDM
        edgedriver_path = _require_existing(LOCAL_EDGE, "MSEDGEDRIVER_PATH")
        options = EdgeOptions()
        options.use_chromium = True
        service = EdgeService(edgedriver_path)
        return webdriver.Edge(service=service, options=options)

    raise ValueError(f"Unsupported browser in config.BROWSER: {browser_name!r}")


@pytest.fixture(scope="session")
def driver():
    browser = getattr(config, "BROWSER", "chrome")
    base_url = getattr(config, "BASE_URL", "https://opennetworks.org/")

    drv = _build_driver(browser)
    print(f"[INFO] Running tests on {browser.capitalize()}")

    drv.get(base_url)
    yield drv
    drv.quit()
