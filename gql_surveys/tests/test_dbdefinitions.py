import sqlalchemy
import sys
import asyncio

# setting path
sys.path.append("../gql_surveys")

import pytest

# from ..uoishelpers.uuid import UUIDColumn

from gql_surveys.DBDefinitions import BaseModel
from gql_surveys.DBDefinitions import UserModel
from gql_surveys.DBDefinitions import AnswerModel, SurveyModel, SurveyTypeModel, QuestionModel, QuestionTypeModel, QuestionValueModel

from shared import prepare_demodata, prepare_in_memory_sqllite, get_demodata


@pytest.mark.asyncio
async def test_table_users_feed():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    stmt = sqlalchemy.select(UserModel)
    async with async_session_maker() as session:
        response = await session.execute(stmt)
        rows = list(response.scalars())
        print(rows)

    data = get_demodata()
    data = list(data["users"])
    result = [
        {"id": u.id, "name": u.name, "surname": u.surname, "email": u.email}
        for u in rows
    ]
    for dr, rr in zip(data, result):
        assert dr == rr


from gql_surveys.DBDefinitions import ComposeConnectionString


def test_connection_string():
    connectionString = ComposeConnectionString()

    assert "://" in connectionString
    assert "@" in connectionString


from gql_surveys.DBDefinitions import UUIDColumn


def test_connection_uuidcolumn():
    col = UUIDColumn(name="name")

    assert col is not None


from gql_surveys.DBDefinitions import startEngine


@pytest.mark.asyncio
async def test_table_start_engine():
    connectionString = "sqlite+aiosqlite:///:memory:"
    async_session_maker = await startEngine(
        connectionString, makeDrop=True, makeUp=True
    )

    assert async_session_maker is not None