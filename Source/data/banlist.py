from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()


class BanList(Base):
    __tablename__ = 'BANLIST'

    user_id = Column('USER_ID', Integer, primary_key=True)
    explain = Column('EXPLAIN', String, nullable=True)
    screen_id = Column('SCREEN_ID', String, nullable=True)


# データベース操作クラス
class BanListDataBase:
    
    def __init__(self) -> None:
        self.dbname = 'sqlite:///Source/data/db/banlist.db'
        self.engine = create_engine(self.dbname, echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.__create_table()

    def __create_table(self) -> None:
        Base.metadata.create_all(self.engine)

    def is_included_banlist(self, user_id: int) -> bool:
        session: Session = self.Session()
        try:
            result = session.query(BanList).filter(BanList.user_id == user_id).first()
            return result is not None
        except SQLAlchemyError as e:
            print(f"Error checking ban list: {e}")
            return False
        finally:
            session.close()
