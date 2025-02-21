from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Enum, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
from datetime import datetime
import enum

# Get database URL from environment variable
DATABASE_URL = os.getenv('DATABASE_URL')

# Create engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class AlertCondition(enum.Enum):
    ABOVE = "above"
    BELOW = "below"

class TransactionType(enum.Enum):
    BUY = "buy"
    SELL = "sell"

class Cryptocurrency(Base):
    __tablename__ = "cryptocurrencies"

    id = Column(Integer, primary_key=True)
    coin_id = Column(String, unique=True)  # CoinGecko ID
    symbol = Column(String)
    name = Column(String)
    current_price = Column(Float)
    market_cap = Column(Float)
    price_change_24h = Column(Float)
    last_updated = Column(DateTime, default=datetime.utcnow)
    prices = relationship("PriceHistory", back_populates="cryptocurrency")
    alerts = relationship("PriceAlert", back_populates="cryptocurrency")
    portfolio_transactions = relationship("PortfolioTransaction", back_populates="cryptocurrency")

class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True)
    cryptocurrency_id = Column(Integer, ForeignKey('cryptocurrencies.id'))
    price = Column(Float)
    timestamp = Column(DateTime)
    cryptocurrency = relationship("Cryptocurrency", back_populates="prices")

class PriceAlert(Base):
    __tablename__ = "price_alerts"

    id = Column(Integer, primary_key=True)
    cryptocurrency_id = Column(Integer, ForeignKey('cryptocurrencies.id'))
    target_price = Column(Float, nullable=False)
    condition = Column(Enum(AlertCondition), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    triggered_at = Column(DateTime, nullable=True)
    cryptocurrency = relationship("Cryptocurrency", back_populates="alerts")

class PortfolioTransaction(Base):
    __tablename__ = "portfolio_transactions"

    id = Column(Integer, primary_key=True)
    cryptocurrency_id = Column(Integer, ForeignKey('cryptocurrencies.id'))
    transaction_type = Column(Enum(TransactionType), nullable=False)
    quantity = Column(Numeric(precision=18, scale=8), nullable=False)
    price_per_coin = Column(Numeric(precision=18, scale=8), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    cryptocurrency = relationship("Cryptocurrency", back_populates="portfolio_transactions")

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()
