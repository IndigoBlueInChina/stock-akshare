import akshare as ak
from datetime import datetime
from typing import List, Optional
# 更新导入语句
from app.models.stock_models import StockInfo, StockQuote, StockFinancial, StockFundFlow, StockHistory
from app.utils.akshare_wrapper import handle_akshare_exception
from app.core.logging import get_logger
from app.utils.cache import cache_result

logger = get_logger(__name__)

class StockService:
    @cache_result()
    @handle_akshare_exception
    async def get_stock_info(self, stock_code: str) -> StockInfo:
        """获取个股基本信息"""
        logger.info(f"获取个股基本信息: {stock_code}")
        # 调用AKShare接口获取个股基本信息
        stock_info = ak.stock_individual_info_em(symbol=stock_code)
        
        # 处理数据并返回
        if stock_info.empty:
            logger.warning(f"未找到股票代码 {stock_code} 的基本信息")
            raise ValueError(f"未找到股票代码 {stock_code} 的基本信息")
        
        # 创建字典用于存储信息
        info_dict = {}
        for _, row in stock_info.iterrows():
            info_dict[row[0]] = row[1]
        
        # 处理数据并返回
        return StockInfo(
            code=stock_code,
            name=info_dict.get("股票简称", ""),
            industry=info_dict.get("行业", None),
            listing_date=info_dict.get("上市时间", None),
            total_market_value=float(info_dict.get("总市值", 0)) if info_dict.get("总市值") else None,
            circulating_market_value=float(info_dict.get("流通市值", 0)) if info_dict.get("流通市值") else None,
            total_share=float(info_dict.get("总股本", 0)) if info_dict.get("总股本") else None,
            circulating_share=float(info_dict.get("流通股", 0)) if info_dict.get("流通股") else None
        )
    
    @handle_akshare_exception
    async def get_stock_quote(self, stock_code: str) -> StockQuote:
        """获取个股实时行情"""
        # 调用AKShare接口获取个股实时行情
        stock_quote = ak.stock_zh_a_spot_em()
        # 筛选指定股票并处理数据
        stock_data = stock_quote[stock_quote['代码'] == stock_code]
        if stock_data.empty:
            raise ValueError(f"未找到股票代码 {stock_code} 的行情数据")
        
        return StockQuote(
            code=stock_code,
            name=stock_data['名称'].values[0],
            price=float(stock_data['最新价'].values[0]),
            change=float(stock_data['涨跌幅'].values[0]),
            # 其他字段处理...
        )
    
    @handle_akshare_exception
    async def get_stock_financial(self, stock_code: str) -> StockFinancial:
        """获取个股财务信息"""
        # 调用AKShare接口获取个股财务信息
        # 处理数据并返回
        pass
    
    @handle_akshare_exception
    async def get_stock_fund_flow(self, stock_code: str) -> StockFundFlow:
        """获取个股资金流向"""
        # 调用AKShare接口获取个股资金流向
        # 处理数据并返回
        pass
    
    @handle_akshare_exception
    async def get_stock_margin(self, stock_code: str) -> dict:
        """获取个股融资融券信息"""
        # 调用AKShare接口获取个股融资融券信息
        # 处理数据并返回
        pass
    
    @cache_result()
    @handle_akshare_exception
    async def get_stock_history(
        self, 
        stock_code: str, 
        period: str = "daily", 
        start_date: Optional[str] = None, 
        end_date: Optional[str] = None
    ) -> List[StockHistory]:
        """
        获取个股历史行情数据
        
        Args:
            stock_code: 股票代码，如"000001"
            period: 周期，可选 daily(日线), weekly(周线), monthly(月线)
            start_date: 开始日期，格式YYYYMMDD，如"20210101"
            end_date: 结束日期，格式YYYYMMDD，如"20210630"
            
        Returns:
            List[StockHistory]: 历史行情数据列表
            
        Raises:
            ValueError: 当获取数据失败或参数错误时抛出
        """
        logger.info(f"获取个股历史行情: {stock_code}, 周期: {period}, 开始日期: {start_date}, 结束日期: {end_date}")
        
        # 验证周期参数
        if period not in ["daily", "weekly", "monthly"]:
            logger.error(f"不支持的周期类型: {period}")
            raise ValueError(f"不支持的周期类型: {period}，支持的类型为daily, weekly, monthly")
        
        # 调用AKShare接口获取历史行情数据，使用前复权(qfq)
        df = ak.stock_zh_a_hist(
            symbol=stock_code, 
            period=period, 
            start_date=start_date, 
            end_date=end_date,
            adjust="qfq"  # 使用前复权数据
        )
        
        if df.empty:
            logger.warning(f"未找到股票代码 {stock_code} 的历史行情数据")
            raise ValueError(f"未找到股票代码 {stock_code} 的历史行情数据")
        
        # 将DataFrame转换为StockHistory对象列表
        result = []
        for _, row in df.iterrows():
            history = StockHistory(
                code=stock_code,
                date=row["日期"],
                open=float(row["开盘"]),
                close=float(row["收盘"]),
                high=float(row["最高"]),
                low=float(row["最低"]),
                volume=int(row["成交量"]),
                amount=float(row["成交额"]),
                amplitude=float(row["振幅"]),
                change_percent=float(row["涨跌幅"]),
                change_amount=float(row["涨跌额"]),
                turnover=float(row["换手率"])
            )
            result.append(history)
        
        return result