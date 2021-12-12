from typing_extensions import Required

#from sqlalchemy.sql.sqltypes import Boolean
from graphene import ObjectType, String, Field, ID, List, DateTime, Mutation, Boolean, Int

from models.FacilitiesRelated.RoomModel import RoomModel
from graphqltypes.Utils import extractSession

class RoomType(ObjectType):
    id = ID()

    lastchange = DateTime()
    externalId = String()

    building = Field('graphqltypes.Building.BuildingType')
    events = List('graphqltypes.Event.EventType')

    def resolve_building(parent, info):
        session = extractSession(info)
        dbRecord = session.query(RoomModel).get(parent.id)
        return dbRecord.building

    def resolve_events(parent, info):
        session = extractSession(info)
        dbRecord = session.query(RoomModel).get(parent.id)
        return dbRecord.events