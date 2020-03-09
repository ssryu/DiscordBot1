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


class JobMasterError(Exception):
    """JobMasterモデルが投げる例外の基底クラス"""


class 職が見つからない(JobMasterError):
    pass


class JobMaster(Base):
    __tablename__ = '職マスタ'

    @classmethod
    def 全件取得(cls, session):
        jobs = session.query(cls.classes.職マスタ).all()
        return jobs

    @classmethod
    def 職名で取得(cls, session, job_name):
        job = session.query(cls.classes.職マスタ).filter(
            cls.classes.職マスタ.職名 == job_name
        ).one_or_none()
        if job is None:
            raise 職が見つからない

        return job

    @classmethod
    def 追加(cls, session, job_name):
        job_record = cls.classes.職マスタ(
            職名=job_name
        )
        session.merge(job_record)
        session.flush()

        try:
            session.commit()
            return
        except InvalidRequestError as e:
            return

    @classmethod
    def 削除(cls, session, job_name):
        target_record = cls.職名で取得(session, job_name)
        session.delete(target_record)
        session.flush()

        try:
            session.commit()
        except InvalidRequestError as e:
            return target_record
        return target_record
