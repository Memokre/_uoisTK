import sqlalchemy
import datetime

from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Integer,
    DateTime,
    ForeignKey,
    Sequence,
    Table,
    Boolean,
)
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()


def UUIDColumn(name=None):
    if name is None:
        return Column(
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sqlalchemy.text("gen_random_uuid()"),
            unique=True,
        )
    else:
        return Column(
            name,
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sqlalchemy.text("gen_random_uuid()"),
            unique=True,
        )


# id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"),)

###########################################################################################################################
#
# zde definujte sve SQLAlchemy modely
# je-li treba, muzete definovat modely obsahujici jen id polozku, na ktere se budete odkazovat
#
###########################################################################################################################


class TopicModel(BaseModel):
    __tablename__ = "actopics"
    id = UUIDColumn()


class LessonTypeModel(BaseModel):
    __tablename__ = "aclessontypes"
    id = UUIDColumn()


class SemesterModel(BaseModel):
    __tablename__ = "acsemesters"
    id = UUIDColumn()


class UserModel(BaseModel):
    __tablename__ = "users"
    id = UUIDColumn()


class GroupModel(BaseModel):
    __tablename__ = "groups"
    id = UUIDColumn()


class Event(BaseModel):
    __tablename__ = "events"
    id = UUIDColumn()


class Facility(BaseModel):
    __tablename__ = "facilities"
    id = UUIDColumn()


class PlannedLessonModel(BaseModel):
    """Defines a lesson which is going to be planned in timetable"""

    __tablename__ = "plan_lessons"

    id = UUIDColumn()
    name = Column(String)
    length = Column(Integer)
    startproposal = Column(DateTime)
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())

    linkedlesson_id = Column(ForeignKey("plan_lessons.id"), nullable=True)
    topic_id = Column(ForeignKey("actopics.id"), nullable=True)
    lessontype_id = Column(ForeignKey("aclessontypes.id"))
    semester_id = Column(ForeignKey("acsemesters.id"), nullable=True)
    event_id = Column(ForeignKey("events.id"), nullable=True)


class UserPlan(BaseModel):
    __tablename__ = "plan_lessons_users"

    id = UUIDColumn()
    user_id = Column(ForeignKey("users.id"))
    planlesson_id = Column(ForeignKey("plan_lessons.id"))


class GroupPlan(BaseModel):
    __tablename__ = "plan_lessons_groups"

    id = UUIDColumn()
    group_id = Column(ForeignKey("groups.id"))
    planlesson_id = Column(ForeignKey("plan_lessons.id"))


class FacilityPlan(BaseModel):
    __tablename__ = "plan_lessons_facilities"

    id = UUIDColumn()
    facility_id = Column(ForeignKey("facilities.id"))
    planlesson_id = Column(ForeignKey("plan_lessons.id"))


###########################################################

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine


async def startEngine(connectionstring, makeDrop=False, makeUp=True):
    """Provede nezbytne ukony a vrati asynchronni SessionMaker"""
    asyncEngine = create_async_engine(connectionstring)

    async with asyncEngine.begin() as conn:
        if makeDrop:
            await conn.run_sync(BaseModel.metadata.drop_all)
            print("BaseModel.metadata.drop_all finished")
        if makeUp:
            await conn.run_sync(BaseModel.metadata.create_all)
            print("BaseModel.metadata.create_all finished")

    async_sessionMaker = sessionmaker(
        asyncEngine, expire_on_commit=False, class_=AsyncSession
    )
    return async_sessionMaker


import os


def ComposeConnectionString():
    """Odvozuje connectionString z promennych prostredi (nebo z Docker Envs, coz je fakticky totez).
    Lze predelat na napr. konfiguracni file.
    """
    user = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("POSTGRES_PASSWORD", "example")
    database = os.environ.get("POSTGRES_DB", "data")
    hostWithPort = os.environ.get("POSTGRES_HOST", "postgres:5432")

    driver = "postgresql+asyncpg"  # "postgresql+psycopg2"
    connectionstring = f"{driver}://{user}:{password}@{hostWithPort}/{database}"

    return connectionstring
