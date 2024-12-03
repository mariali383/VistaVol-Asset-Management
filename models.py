from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, UniqueConstraint, Enum
from db import Base
from typing import Literal, get_args

Option_Type = Literal["Put", "Call"]

class SHFE_DAILY_ONE(Base):
    __tablename__ = 'shfe_daily_one'
 
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, nullable=False, autoincrement=True)
    trade_date: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    合约代码: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    开盘价: Mapped[float] = mapped_column(nullable=False)
    最高价: Mapped[float] = mapped_column(nullable=False)
    最低价: Mapped[float] = mapped_column(nullable=False)
    收盘价: Mapped[float] = mapped_column(nullable=False)
    前结算价: Mapped[float] = mapped_column(nullable=False)
    结算价: Mapped[float] = mapped_column(nullable=False)
    涨跌: Mapped[float] = mapped_column(nullable=False)
    涨跌1: Mapped[float] = mapped_column(nullable=False)
    涨跌2: Mapped[float] = mapped_column(nullable=False)
    成交量: Mapped[float] = mapped_column(nullable=False)
    持仓量: Mapped[float] = mapped_column(nullable=False)
    持仓量变化: Mapped[float] = mapped_column(nullable=False)
    成交额: Mapped[float] = mapped_column(nullable=False)
    德尔塔: Mapped[float] = mapped_column(nullable=False)
    行权量: Mapped[float] = mapped_column(nullable=False)
    __table_args__ = (
        UniqueConstraint('trade_date', '合约代码', name='idx_date_contract'),  # Unique index
    )

class SHFE_DAILY_TWO(Base):
    __tablename__ = 'shfe_daily_two'
 
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, nullable=False, autoincrement=True)
    trade_date: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    合约系列: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    成交量: Mapped[float] = mapped_column(nullable=False, index=True)
    持仓量: Mapped[float] = mapped_column(nullable=False)
    持仓量变化: Mapped[float] = mapped_column(nullable=False)
    成交额: Mapped[float] = mapped_column(nullable=False)
    行权量: Mapped[float] = mapped_column(nullable=False)
    隐含波动率: Mapped[float] = mapped_column(nullable=False)
    __table_args__ = (
        UniqueConstraint('trade_date', '合约系列', name='idx_date_contract'),  # Unique index
    )
    
# have not filled the below tables... 
class Contracts(Base):
    __tablename__ = 'contracts'
    
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, nullable=False, autoincrement=True)
    合约: Mapped[str] = mapped_column(String(100), nullable=False) # contract
    看涨合约_买量: Mapped[int] = mapped_column(nullable=False)
    看涨合约_买价: Mapped[float] = mapped_column(nullable=False)
    看涨合约_最新价: Mapped[float] = mapped_column(nullable=False)
    看涨合约_卖价: Mapped[float] = mapped_column(nullable=False)
    看涨合约_卖量: Mapped[int] = mapped_column(nullable=False)
    看涨合约_持仓量: Mapped[int] = mapped_column(nullable=False)
    看涨合约_涨跌: Mapped[float] = mapped_column(nullable=False)
    行权价: Mapped[int] = mapped_column(nullable=False)
    看涨合约_看涨期权合约: Mapped[str] = mapped_column(String(100), nullable=False)
    看跌合约_买量: Mapped[int] = mapped_column(nullable=False)
    看跌合约_买价: Mapped[float] = mapped_column(nullable=False)
    看跌合约_最新价: Mapped[float] = mapped_column(nullable=False)
    看跌合约_卖价: Mapped[float] = mapped_column(nullable=False)
    看跌合约_卖量: Mapped[int] = mapped_column(nullable=False)
    看跌合约_持仓量: Mapped[int] = mapped_column(nullable=False)
    看跌合约_涨跌: Mapped[float] = mapped_column(nullable=False)
    看跌合约_看跌期权合约: Mapped[str] = mapped_column(String(100), nullable=False)
    
class Contract(Base):
    __tablename__ = 'contract'
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, nullable=False, autoincrement=True)
    # Contract
    合约: Mapped[str] = mapped_column(String(100), nullable=False)
    # contract_code
    看跌合约_看跌期权合约: Mapped[str] = mapped_column(String(100), nullable=False)
    option_type: Mapped[Option_Type] = mapped_column(Enum(
      *get_args(Option_Type),
      name="option_type",
      create_constraint=True,
      validate_strings=True,
    ))
    date: Mapped[str] = mapped_column(String(100), nullable=False)
    open: Mapped[float] = mapped_column(nullable=False)
    high: Mapped[float] = mapped_column(nullable=False)
    low: Mapped[float] = mapped_column(nullable=False)
    close: Mapped[float] = mapped_column(nullable=False)
    volume: Mapped[float] = mapped_column(nullable=False)
