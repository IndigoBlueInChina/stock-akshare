import akshare as ak
import pandas as pd
from datetime import datetime
from typing import List, Optional
from app.models.news_models import InteractiveQuestion, GlobalFinanceNews, CLSTelegraph
# 修改这一行，从 akshare_wrapper 导入 handle_akshare_exception
from app.utils.akshare_wrapper import handle_akshare_exception
from app.core.logging import get_logger
from app.utils.cache import cache_result

logger = get_logger(__name__)

class NewsService:
    """资讯服务"""
    
    @cache_result()
    @handle_akshare_exception
    async def get_interactive_questions(self, symbol: str) -> List[InteractiveQuestion]:
        """
        获取互动易提问数据
        
        Args:
            symbol: 股票代码，如"002594"
            
        Returns:
            List[InteractiveQuestion]: 互动易提问数据列表
        """
        logger.info(f"获取互动易提问数据: {symbol}")
        
        # 标准化股票代码（去掉市场前缀）
        if symbol.startswith(("sh", "sz", "bj")):
            symbol = symbol[2:]
        
        # 调用AKShare接口获取互动易提问数据
        df = ak.stock_irm_cninfo(symbol=symbol)
        
        if df.empty:
            logger.warning(f"未获取到股票 {symbol} 的互动易提问数据")
            return []
        
        # 将DataFrame转换为InteractiveQuestion对象列表
        result = []
        for _, row in df.iterrows():
            # 处理可能的NaN值
            industry = row["行业"] if pd.notna(row["行业"]) else None
            industry_code = row["行业代码"] if pd.notna(row["行业代码"]) else None
            questioner_id = row["提问者编号"] if pd.notna(row["提问者编号"]) else None
            question_id = row["问题编号"] if pd.notna(row["问题编号"]) else None
            answer_id = row["回答ID"] if pd.notna(row["回答ID"]) else None
            answer_content = row["回答内容"] if pd.notna(row["回答内容"]) else None
            answerer = row["回答者"] if pd.notna(row["回答者"]) else None
            
            # 转换日期时间格式
            question_time = row["提问时间"].to_pydatetime() if pd.notna(row["提问时间"]) else datetime.now()
            update_time = row["更新时间"].to_pydatetime() if pd.notna(row["更新时间"]) else datetime.now()
            
            question = InteractiveQuestion(
                stock_code=row["股票代码"],
                stock_name=row["公司简称"],
                industry=industry,
                industry_code=industry_code,
                question=row["问题"],
                questioner=row["提问者"],
                source=row["来源"],
                question_time=question_time,
                update_time=update_time,
                questioner_id=questioner_id,
                question_id=question_id,
                answer_id=answer_id,
                answer_content=answer_content,
                answerer=answerer
            )
            result.append(question)
        
        return result
    
    @cache_result()
    @handle_akshare_exception
    async def get_global_finance_news(self) -> List[GlobalFinanceNews]:
        """
        获取全球财经快讯数据
        
        Returns:
            List[GlobalFinanceNews]: 全球财经快讯数据列表
        """
        logger.info("获取全球财经快讯数据")
        
        # 调用AKShare接口获取全球财经快讯数据
        df = ak.stock_info_global_em()
        
        if df.empty:
            logger.warning("未获取到全球财经快讯数据")
            return []
        
        # 将DataFrame转换为GlobalFinanceNews对象列表
        result = []
        for _, row in df.iterrows():
            news = GlobalFinanceNews(
                title=row["标题"],
                summary=row["摘要"],
                publish_time=row["发布时间"],
                link=row["链接"],
                update_time=datetime.now()
            )
            result.append(news)
        
        return result
    
    @cache_result()
    @handle_akshare_exception
    async def get_cls_telegraph(self, symbol: str = "全部") -> List[CLSTelegraph]:
        """
        获取财联社电报数据
        
        Args:
            symbol: 类型，可选值为"全部"或"重点"，默认为"全部"
            
        Returns:
            List[CLSTelegraph]: 财联社电报数据列表
        """
        logger.info(f"获取财联社电报数据: {symbol}")
        
        # 调用AKShare接口获取财联社电报数据
        df = ak.stock_info_global_cls(symbol=symbol)
        
        if df.empty:
            logger.warning(f"未获取到财联社电报数据: {symbol}")
            return []
        
        # 将DataFrame转换为CLSTelegraph对象列表
        result = []
        for _, row in df.iterrows():
            # 处理可能的NaN值
            title = row["标题"] if pd.notna(row["标题"]) else ""
            content = row["内容"] if pd.notna(row["内容"]) else ""
            publish_date = row["发布日期"] if pd.notna(row["发布日期"]) else ""
            publish_time = row["发布时间"] if pd.notna(row["发布时间"]) else ""
            
            telegraph = CLSTelegraph(
                title=title,
                content=content,
                publish_date=publish_date,
                publish_time=publish_time,
                update_time=datetime.now()
            )
            result.append(telegraph)
        
        return result