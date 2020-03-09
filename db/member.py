import logging
import uuid

import pytz
from sqlalchemy import false
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.automap import automap_base

from db.session import engine, session

logger = logging.getLogger(__name__)

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.query = session.query_property()


class MemberError(Exception):
    """Memberモデルが投げる例外の基底クラス"""


class メンバーが見つからない(MemberError):
    pass


class 職が見つからない(MemberError):
    pass


class Member(Base):
    __tablename__ = 'メンバー'

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
    def UserIDでメンバーを取得(cls, session, user_id):
        member = session.query(cls.classes.メンバー).filter(
            cls.classes.メンバー.user_id == str(user_id),
            cls.classes.メンバー.脱退済 == false()
        ).one_or_none()
        if member is None:
            raise メンバーが見つからない
        return member

    @classmethod
    def UUIDでメンバー履歴を取得(cls, session, id):
        member_history = session.query(cls.classes.メンバー履歴).filter(
            cls.classes.メンバー履歴.UUIDv4 == id
        ).order_by(cls.classes.メンバー履歴.created_at.desc()).first()
        return member_history

    @classmethod
    def 職業名で職を取得(cls, session, 職業名):
        job = session.query(cls.classes.職マスタ).filter(
            cls.classes.職マスタ.職名 == 職業名
        ).one_or_none()
        if job is None:
            raise 職が見つからない
        return job

    @classmethod
    def 戦闘力更新(cls, session, user_id, 戦闘力):
        member = cls.UserIDでメンバーを取得(session, user_id)
        member_history = cls.UUIDでメンバー履歴を取得(session, member.メンバー履歴_UUIDv4)

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
    def 職業変更(cls,session, user_id, 職業名):
        member = cls.UserIDでメンバーを取得(session, user_id)
        member_history = cls.UUIDでメンバー履歴を取得(session, member.メンバー履歴_UUIDv4)
        job = cls.職業名で職を取得(session, 職業名)

        new_history_id = uuid.uuid4()
        new_history = cls.classes.メンバー履歴(
            UUIDv4=new_history_id,
            user_id=str(user_id),
            家門名=member_history.家門名,
            戦闘力=member_history.戦闘力,
            職マスタ_職名=job.職名
        )
        session.add(new_history)
        session.flush()

        # メンバーマスタ側に最新の履歴を示すように変更を加える
        member.メンバー履歴_UUIDv4 = new_history_id
        session.add(member)
        session.flush()

        try:
            session.commit()
        except InvalidRequestError as e:
            return
        return

    @classmethod
    def 除隊(cls, session, user_id):
        member = cls.UserIDでメンバーを取得(session, user_id)

        member.脱退済 = True
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
