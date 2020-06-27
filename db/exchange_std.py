import logging
import uuid

import sqlalchemy
from sqlalchemy import desc
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import relationship


from db.session import engine, session

logger = logging.getLogger(__name__)

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.query = session.query_property()

class ExchangeStandardError(Exception):
    """ExchangeStandardモデルが投げる例外の基底クラス"""


class 基準時刻が見つからない(ExchangeStandardError):
    pass


class ExchangeStandard(Base):
    __tablename__ = '取引所基準時刻'

    @classmethod
    def 最新の取引所基準時刻を取得(cls, session):
        result = session.query(cls.classes.取引所基準時刻).order_by(desc(cls.classes.取引所基準時刻.created_at)).first()
        if not result:
            raise 基準時刻が見つからない
        return result.std_time

    @classmethod
    def 更新(cls, session, std_time):
        record = cls.classes.取引所基準時刻(
            std_time=std_time
        )
        session.add(record)
        session.flush()
        try:
            session.commit()
        except InvalidRequestError as e:
            return
        return True
