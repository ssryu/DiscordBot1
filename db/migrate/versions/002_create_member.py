from sqlalchemy import *
from migrate import *

meta = MetaData()

memberTable = Table(
    'member', meta,

    Column('user_id', VARCHAR(32), primary_key=True),
    Column('member_history_uuidv4', VARCHAR(36), unique=True, nullable=False)
)


memberHistoryTable = Table(
    'member_history', meta,

    Column('UUIDv4', VARCHAR(36), nullable=False),
    Column('user_id', VARCHAR(32), nullable=False),
    Column('家門名', VARCHAR(45), nullable=False),
    Column('戦闘力', INTEGER, nullable=False),
    Column('職マスタ_職名', VARCHAR(50), nullable=False),
    Column('大砲', ),
    Column('火箭'),
    Column('象'),
    Column('created_at', DateTime, nullable=False)
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta.bind = migrate_engine
    table.create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    table.drop()

