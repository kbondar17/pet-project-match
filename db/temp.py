# # from weedly.db.models import Base, users_n_feeds, UserCategory
# #
# # # for e in users_n_feeds.c:
# # #     print(e)
# #
# # print('--')
# # print(users_n_feeds.foreign_keys)
# #
# # # print(dir(Base.metadata))
# # # print(Base.metadata.naming_convention)
#
#
# from sqlalchemy import *
# engine = create_engine('sqlite:///:memory:')
# metadata_obj = MetaData()
#
#
#
# financial_info = Table(
#     'financial_info',
#     metadata_obj,
#     Column('id', Integer, primary_key=True),
#     Column('value', String(100), nullable=False),
#     schema='remote_banks'
# )
#
# customer = Table(
#     "customer",
#     metadata_obj,
#     Column('id', Integer, primary_key=True),
#     Column('financial_info_id', ForeignKey("remote_banks.financial_info.id")),
#     schema='customers_info'
# )
#
#
# print(metadata_obj.tables.keys())
#
#
#
#
#
