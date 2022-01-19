""" Pytest fixitures for tests """
import tempfile

import pytest
import os

from nowcasting_forecast.database.connection import DatabaseConnection
from nowcasting_forecast.database.models import Base
from nowcasting_forecast.database.fake import make_fake_forecast, make_fake_forecasts


@pytest.fixture
def forecast(db_session):
    """Pytest fixture of one fake forecast"""
    # create and add
    f = make_fake_forecast(gsp_id=1)
    db_session.add(f)

    return f


@pytest.fixture
def forecasts(db_session):
    """Pytest fixture of 338 fake forecasts"""
    # create
    f = make_fake_forecasts(gsp_ids=list(range(0, 338)))
    db_session.add_all(f)

    return f


@pytest.fixture
def db_connection():
    """Pytest fixture for a database connection"""
    with tempfile.NamedTemporaryFile(suffix="db") as tmp:
        url = f"sqlite:///{tmp.name}.db"
        os.environ["DB_URL"] = url
        connection = DatabaseConnection(url=url)
        Base.metadata.create_all(connection.engine)

        yield connection


@pytest.fixture(scope="function", autouse=True)
def db_session(db_connection):
    """Creates a new database session for a test."""

    with db_connection.get_session() as s:
        s.begin()
        yield s

        s.rollback()