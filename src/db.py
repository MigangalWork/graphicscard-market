from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.engine import Engine



DATABASE_URL: str = "sqlite:///./example.db"
engine: Engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
session_maker: sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class ExecutionCase(Base):
    __tablename__ = 'execution_case'
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, server_default=func.now())

    market_histories = relationship("MarketHistory", back_populates="execution_case")
    transactions = relationship("Transaction", back_populates="execution_case")

class MarketHistory(Base):
    __tablename__ = 'market_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    iteration = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    execution_case_id = Column(Integer, ForeignKey('execution_case.id'), nullable=False)
    execution_case = relationship("ExecutionCase", back_populates="market_histories")

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    iteration = Column(Integer, nullable=False)
    agent_name = Column(String, nullable=False)
    action = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    execution_case_id = Column(Integer, ForeignKey('execution_case.id'), nullable=False)
    execution_case = relationship("ExecutionCase", back_populates="transactions")

Base.metadata.create_all(bind=engine)
