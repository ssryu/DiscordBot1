from sqlalchemy import *
from migrate import *

meta = MetaData()

table = Table(
    'replace_word', meta,
    Column('id', BIGINT(), primary_key=True),
    Column('keyword', TEXT, nullable=False),
    Column('replace_to', TEXT, nullable=False))


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta.bind = migrate_engine
    table.create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    table.drop()

