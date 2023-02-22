import atexit
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, create_engine, func 
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import EmailType


PG_DSN = 'postgresql://artur:8114@127.0.0.1:5431/flask_db'

engine = create_engine(PG_DSN) # Подключение к БД

Base = declarative_base() # Создаем базовый класс для модели
Session = sessionmaker(bind=engine) # Создаем базовый класс для подключения


class User(Base):

    __tablename__ = 'app_users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(30), nullable=False, unique=True, index=True)
    email = Column(EmailType, nullable=False, unique=True)
    password = Column(String(60), nullable=False)
    creation_time = Column(DateTime, default=func.now())
    ads = relationship('Ad')


class Ad(Base):
    
    __tablename__ = 'ads'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(String(600), nullable=False)
    creation_time = Column(DateTime, default=func.now())
    id_user = Column(Integer, ForeignKey('app_users.id', ondelete="CASCADE"))
    user = relationship("User", lazy="joined")


Base.metadata.create_all(bind=engine) # Инструкция для создания всех таблиц

atexit.register(engine.dispose) # После завершения разрывать связь