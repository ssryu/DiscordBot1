import logging
import uuid

import pytz
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.automap import automap_base

from db.session import engine, session

logger = logging.getLogger(__name__)

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.query = session.query_property()


class Member(Base):
    __tablename__ = 'メンバー'

    @classmethod
    def all(cls, session):
        return session.query(cls.classes.メンバー).all()

    @classmethod
    def find(cls, session, user_id):
        a = session.query(cls.classes.メンバー).filter(cls.classes.メンバー.user_id == str(user_id)).all()
        return a

    @classmethod
    def 指定期間における履歴取得(cls, session, user_id, start, end):
        utc = pytz.timezone('UTC')
        start.astimezone(utc)
        end.astimezone(utc)

        a = session.query(cls.classes.メンバー履歴).filter(
            cls.classes.メンバー履歴.user_id == str(user_id),
            cls.classes.メンバー履歴.created_at >= start,
            cls.classes.メンバー履歴.created_at < end
        ).order_by(cls.classes.メンバー履歴.created_at).all()
        return a

    @classmethod
    def 戦闘力更新(cls, session, user_id, 戦闘力):
        member = session.query(cls.classes.メンバー).filter(
            cls.classes.メンバー.user_id == str(user_id)
        ).one()

        member_history = session.query(cls.classes.メンバー履歴).filter(
            cls.classes.メンバー履歴.UUIDv4 == member.メンバー履歴_UUIDv4
        ).order_by(cls.classes.メンバー履歴.created_at.desc()).first()

        new_history_id = uuid.uuid4()
        new_history = cls.classes.メンバー履歴(
            UUIDv4=new_history_id,
            user_id=str(user_id),
            家門名=member_history.家門名,
            戦闘力=戦闘力,
            職マスタ_職名=member_history.職マスタ_職名
        )
        session.add(new_history)
        session.flush()

        member.メンバー履歴_UUIDv4 = new_history_id
        session.add(member)
        session.flush()

        try:
            session.commit()
        except InvalidRequestError as e:
            return
        return

    @classmethod
    def 登録(cls, session, user_id, 家門名, 戦闘力, 職名):
        history_id = uuid.uuid4()

        history_record = cls.classes.メンバー履歴(
            UUIDv4=history_id,
            user_id=str(user_id),
            家門名=家門名,
            戦闘力=戦闘力,
            職マスタ_職名=職名
        )
        session.add(history_record)
        session.flush()

        member_record = cls.classes.メンバー(
            user_id=str(user_id),
            メンバー履歴_UUIDv4=history_id
        )
        session.merge(member_record)
        session.flush()

        try:
            session.commit()
        except InvalidRequestError as e:
            return

        return True
