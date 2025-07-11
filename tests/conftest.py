"""Configuration for pytest."""
import asyncio

import pytest

from src.configuration import Configuration

from .utils.alembic import alembic_config_from_url


@pytest.fixture()
def alembic_config():
    """Alembic configuration object, bound to temporary database."""
    conf = Configuration()
    return alembic_config_from_url(conf.db.build_connection_str())


@pytest.fixture()
def event_loop():
    """Fixture for event loop."""
    return asyncio.new_event_loop()
