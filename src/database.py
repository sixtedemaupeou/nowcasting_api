""" Functions to read from the database and format """
import logging
import os

from nowcasting_datamodel.connection import DatabaseConnection
from nowcasting_datamodel.models import Forecast, ManyForecasts
from nowcasting_datamodel.read import (
    get_all_gsp_ids_latest_forecast,
    get_latest_forecast,
    get_latest_national_forecast,
)
from sqlalchemy.orm.session import Session

logger = logging.getLogger(__name__)


def get_forecasts_from_database(session: Session) -> ManyForecasts:
    """Get forecasts from database for all GSPs"""
    # sql sqlalchemy objects
    forecasts = get_all_gsp_ids_latest_forecast(session=session)

    # change to pydantic objects
    forecasts = [Forecast.from_orm(forecast) for forecast in forecasts]

    # return as many forecasts
    return ManyForecasts(forecasts=forecasts)


def get_forecasts_for_a_specific_gsp_from_database(session: Session, gsp_id) -> Forecast:
    """Get forecasts for on GSP from database"""
    # get forecast from database
    forecast = get_latest_forecast(session=session, gsp_id=gsp_id)

    return Forecast.from_orm(forecast)


def get_session():
    """Get database settion"""
    connection = DatabaseConnection(url=os.getenv("DB_URL", "not_set"))

    with connection.get_session() as s:
        yield s


def get_latest_national_forecast_from_database(session: Session) -> Forecast:
    """Get the national level forecast from the database"""

    logger.debug("Getting latest national forecast")

    forecast = get_latest_national_forecast(session=session)
    logger.debug(forecast)
    return Forecast.from_orm(forecast)
