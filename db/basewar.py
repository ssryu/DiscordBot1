from datetime import datetime, time
import logging
import uuid

import pytz
import sqlalchemy
from sqlalchemy import or_, cast, true, desc, asc, false
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import relationship

from db.session import engine, session

logger = logging.getLogger(__name__)

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.query = session.query_property()


class BaseWarError(Exception):
    """拠点戦モデルが投げる例外の基底クラス"""


class メンバーが見つからない(BaseWarError):
    pass


class 参加受付中の拠点戦がない(BaseWarError):
    pass


class 参加者がいない(BaseWarError):
    pass


class 参加種別が不正(BaseWarError):
    pass


class 参加VC状況が不正(BaseWarError):
    pass


class BaseWar(Base):
    __tablename__ = '拠点戦'

    @classmethod
    def 拠点戦情報を登録する(cls, session, map_id, date):
        tz_utc = pytz.timezone('UTC')
        dt_native = datetime.combine(date, time())
        utc_date = tz_utc.localize(dt_native)

        basewar = cls.classes.拠点戦(
            日付=utc_date,
            拠点マップ_マップマスタ_id=map_id,
            参加申請受付可否=True
        )
        session.merge(basewar)
        session.flush()

        try:
            session.commit()
        except InvalidRequestError as e:
            return
        return

    @classmethod
    def 拠点戦の参加を締め切る(cls, session, date):
        tz_utc = pytz.timezone('UTC')
        dt_native = datetime.combine(date, time())
        utc_date = tz_utc.localize(dt_native)

        拠点戦 = session.query(cls.classes.拠点戦).filter(
            cls.classes.拠点戦.日付 == utc_date,
            cls.classes.拠点戦.参加申請受付可否 == true()
        ).one_or_none()
        if 拠点戦 is None:
            raise 参加受付中の拠点戦がない

        basewar = cls.classes.拠点戦(
            日付=拠点戦.日付,
            拠点マップ_マップマスタ_id=拠点戦.拠点マップ_マップマスタ_id,
            参加申請受付可否=False
        )
        session.merge(basewar)
        session.flush()

        try:
            session.commit()
        except InvalidRequestError as e:
            return
        return

    @classmethod
    def 拠点戦取得(cls, session, date):
        tz_utc = pytz.timezone('UTC')
        dt_native = datetime.combine(date, time())
        utc_date = tz_utc.localize(dt_native)

        a = session.query(cls.classes.拠点戦).filter(
            cls.classes.拠点戦.日付 == utc_date
        ).one_or_none()

        return a

    @classmethod
    def 参加(cls, session, user_id, date, 参加種別, 参加VC状況):
        tz_utc = pytz.timezone('UTC')
        dt_native = datetime.combine(date, time())
        utc_date = tz_utc.localize(dt_native)

        メンバー = session.query(cls.classes.メンバー).filter(
            cls.classes.メンバー.user_id == str(user_id),
            cls.classes.メンバー.脱退済 == false(),
        ).one_or_none()
        if メンバー is None:
            raise メンバーが見つからない

        拠点戦 = session.query(cls.classes.拠点戦).filter(
            cls.classes.拠点戦.日付 == utc_date,
            cls.classes.拠点戦.参加申請受付可否 == true()
        ).order_by(cls.classes.拠点戦.日付).one_or_none()
        if 拠点戦 is None:
            raise 参加受付中の拠点戦がない

        参加種別マスタレコード = session.query(cls.classes.参加種別マスタ).filter(
            cls.classes.参加種別マスタ.id == 参加種別
        ).one_or_none()
        if 参加種別マスタレコード is None:
            raise 参加種別が不正

        参加VC状況マスタ = session.query(cls.classes.参加VC状況マスタ).filter(
            cls.classes.参加VC状況マスタ.id == 参加VC状況
        ).one_or_none()
        if 参加VC状況マスタ is None:
            raise 参加VC状況が不正

        参加 = cls.classes.拠点戦参加(
            拠点戦_日付=拠点戦.日付,
            メンバー_user_id=str(user_id),
            参加種別マスタ_id=参加種別マスタレコード.id,
            参加VC状況マスタ_id=参加VC状況マスタ.id
        )
        session.merge(参加)
        session.flush()

        try:
            session.commit()
            return 拠点戦
        except InvalidRequestError as e:
            return

    @classmethod
    def 参加者情報取得(cls, session, date):
        tz_utc = pytz.timezone('UTC')
        dt_native = datetime.combine(date, time())
        utc_date = tz_utc.localize(dt_native)

        拠点戦 = session.query(cls.classes.拠点戦).filter(
            cls.classes.拠点戦.日付 == utc_date,
            cls.classes.拠点戦.参加申請受付可否 == true()
        ).order_by(cls.classes.拠点戦.日付).one_or_none()
        if 拠点戦 is None:
            raise 参加受付中の拠点戦がない

        拠点戦参加 = session.query(cls.classes.拠点戦参加).filter(
            cls.classes.拠点戦参加.拠点戦_日付 == utc_date,
            cls.classes.メンバー.脱退済 == false()
        ).join(
            cls.classes.メンバー
        ).join(
            cls.classes.メンバー履歴
        ).order_by(
            asc(cls.classes.拠点戦参加.参加VC状況マスタ_id),
            desc(cls.classes.メンバー履歴.戦闘力)
        ).all()

        if len(拠点戦参加) <= 0:
            raise 参加者がいない

        return 拠点戦参加
