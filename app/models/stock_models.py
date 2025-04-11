from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class StockInfo(BaseModel):
    """个股基本信息模型"""
    code: str
    name: str
    industry: Optional[str] = None
    listing_date: Optional[str] = None
    total_market_value: Optional[float] = None
    circulating_market_value: Optional[float] = None
    total_share: Optional[float] = None
    circulating_share: Optional[float] = None
    
class StockQuote(BaseModel):
    """个股实时行情模型"""
    code: str
    name: str
    price: float
    change: float
    change_percent: float
    open: float
    high: float
    low: float
    volume: int
    amount: float
    turnover_rate: float
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    market_cap: Optional[float] = None
    update_time: datetime
    
class StockFinancial(BaseModel):
    """个股财务信息模型"""
    code: str
    name: str
    eps: Optional[float] = None
    bvps: Optional[float] = None
    roe: Optional[float] = None
    revenue: Optional[float] = None
    revenue_yoy: Optional[float] = None
    net_profit: Optional[float] = None
    net_profit_yoy: Optional[float] = None
    report_date: Optional[datetime] = None
    
class StockFundFlow(BaseModel):
    """个股资金流向模型"""
    code: str
    name: str
    date: datetime
    main_net_inflow: float
    main_net_inflow_percent: float
    super_large_net_inflow: float
    large_net_inflow: float
    medium_net_inflow: float
    small_net_inflow: float

class StockHistory(BaseModel):
    """个股历史行情数据模型"""
    code: str
    date: str
    open: float
    close: float
    high: float
    low: float
    volume: int  # 成交量(手)
    amount: float  # 成交额(元)
    amplitude: float  # 振幅(%)
    change_percent: float  # 涨跌幅(%)
    change_amount: float  # 涨跌额(元)
    turnover: float  # 换手率(%)