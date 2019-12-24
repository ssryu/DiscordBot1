import logging

from db.session import Base

logger = logging.getLogger(__name__)


class ReplaceWord(Base):
    __tablename__ = 'replace_word'

    @classmethod
    def find(cls, session):
        """ find record by id """
        tbl = cls.classes.replace_word
        return session.query(tbl).all()
