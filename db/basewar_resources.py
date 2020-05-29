from datetime import datetime, time
import logging
import uuid

import pytz
import sqlalchemy
from sqlalchemy import or_, cast, true, desc, asc, false
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db.session import engine, session

logger = logging.getLogger(__name__)

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.query = session.query_property()


class BaseWarResourcesError(Exception):
    """拠点戦資材モデルが投げる例外の基底クラス"""


class メンバーが見つからない(BaseWarResourcesError):
    pass


class BaseWarResources(Base):
    __tablename__ = '拠点戦資材'

    @classmethod
    def 全資材申告(cls, session, user_id, resource1, resource2, resource3):
        member = session.query(cls.classes.メンバー).filter(
            cls.classes.メンバー.user_id == str(user_id),
            cls.classes.メンバー.脱退済 == false()
        ).one_or_none()
        if member is None:
            raise メンバーが見つからない

        resource_record = cls.classes.拠点戦資材(
            user_id=str(user_id),
            生命の粉=resource1,
            頑丈な原木=resource2,
            黒い水晶の原石=resource3
        )
        session.merge(resource_record)
        session.flush()

        try:
            session.commit()
        except InvalidRequestError as e:
            return

        return member

    @classmethod
    def 資材集計(cls, session):
        a = session.query(
            func.sum(cls.classes.拠点戦資材.生命の粉).label('生命の粉'),
            func.sum(cls.classes.拠点戦資材.頑丈な原木).label('頑丈な原木'),
            func.sum(cls.classes.拠点戦資材.黒い水晶の原石).label('黒い水晶の原石')
        ).one_or_none()

        return a
