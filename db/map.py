import logging
import uuid

import sqlalchemy
from sqlalchemy import or_, cast
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import relationship

from db.session import engine, session

logger = logging.getLogger(__name__)

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.query = session.query_property()


class Map(Base):
    __tablename__ = 'マップマスタ'

    @classmethod
    def マップidまたはマップ名で検索(cls, session, q):
        a = session.query(cls.classes.マップマスタ).filter(
            or_(
                cast(cls.classes.マップマスタ.id, sqlalchemy.String) == f"{q}",
                cls.classes.マップマスタ.マップ名.like(f"%{q}%")
            )
        ).all()
        return a

    @classmethod
    def マップIDで拠点情報を取得(cls, session, id):
        a = session.query(cls.classes.マップマスタ).filter(
            cls.classes.マップマスタ.id == id
        ).one_or_none()

        return a
