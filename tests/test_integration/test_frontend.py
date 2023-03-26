from contextlib import contextmanager
from time import sleep

import pytest
from playwright.sync_api import Page, expect

LOCAL_TEST = False

PORT = "8503" if LOCAL_TEST else "8699"


@pytest.fixture(scope="module", autouse=True)
def before_module():
    # Run the streamlit app before each module
    with run_streamlit():
        yield


@pytest.fixture(scope="function", autouse=True)
def before_test(page: Page):
    page.goto(f"localhost:{PORT}")

    # give the page time to load
    sleep(5)


@contextmanager
def run_streamlit():
    """Run the streamlit app at app.py on port 8599"""
    import subprocess

    if LOCAL_TEST:
        try:
            yield 1
        finally:
            pass
    else:
        p = subprocess.Popen(
            [
                "streamlit",
                "run",
                "app.py",
                "--server.port",
                PORT,
                "--server.headless",
                "true",
            ]
        )

        # give the app time to run
        sleep(5)

        try:
            yield 1
        finally:
            p.kill()


def test_marker_click(page: Page):
    # Check page title
    expect(page.get_by_text("Welcome to Coffee DB!")).to_be_visible()
