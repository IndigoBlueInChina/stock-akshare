import akshare as ak
import pandas as pd
import math
from datetime import datetime
from typing import List, Optional
from app.models.sector_models import (
    ConceptBoard, IndustryBoard, BoardSpot, 
    ConceptBoardSpot, IndustryBoardSpot,
    ConceptBoardConstituent, IndustryBoardConstituent
)
from app.utils.akshare_wrapper import handle_akshare_exception
from app.core.logging import get_logger
from app.utils.cache import cache_result

logger = get_logger(__name__)

# 添加一个辅助函数来处理特殊浮点值
def safe_float(value, default=None):
    """
    安全地将值转换为浮点数，处理NaN和Infinity
    
    Args:
        value: 要转换的值
        default: 如果转换失败或值为特殊值时返回的默认值
        
    Returns:
        float: 转换后的浮点数或默认值
    """
    if pd.isna(value):
        return default
    
    try:
        float_value = float(value)
        if math.isnan(float_value) or math.isinf(float_value):
            return default
        return float_value
    except (ValueError, TypeError):
        return default

class SectorService:
    """板块服务"""
    
    @cache_result()
    @handle_akshare_exception
    async def get_concept_boards(self) -> List[ConceptBoard]:
        """
        获取概念板块列表及实时行情
        
        Returns:
            List[ConceptBoard]: 概念板块列表
        """
        logger.info("获取概念板块列表")
        
        # 调用AKShare接口获取概念板块数据
        df = ak.stock_board_concept_name_em()
        
        if df.empty:
            logger.warning("未获取到概念板块数据")
            return []
        
        # 将DataFrame转换为ConceptBoard对象列表
        result = []
        for _, row in df.iterrows():
            # 使用safe_float函数处理所有浮点值
            market_value = int(row["总市值"]) if not pd.isna(row["总市值"]) else None
            
            board = ConceptBoard(
                rank=int(row["排名"]),
                name=row["板块名称"],
                code=row["板块代码"],
                price=safe_float(row["最新价"], 0),
                change=safe_float(row["涨跌额"], 0),
                change_percent=safe_float(row["涨跌幅"], 0),
                market_value=market_value,
                turnover_rate=safe_float(row["换手率"], 0),
                up_count=int(row["上涨家数"]),
                down_count=int(row["下跌家数"]),
                leading_stock=row["领涨股票"],
                leading_stock_change_percent=safe_float(row["领涨股票-涨跌幅"], 0),
                update_time=datetime.now()
            )
            result.append(board)
        
        return result
    
    @cache_result()
    @handle_akshare_exception
    async def get_concept_board(self, board_code: str, name: Optional[str] = None) -> Optional[ConceptBoard]:
        """
        获取单个概念板块信息
        
        Args:
            board_code: 板块代码，如"BK0715"
            name: 板块名称，如"可燃冰"，当提供名称时，会尝试通过名称查找板块代码
            
        Returns:
            Optional[ConceptBoard]: 概念板块信息，如果未找到则返回None
        """
        logger.info(f"获取单个概念板块 get_concept_board : {board_code}")
        
        # 如果提供了名称，尝试通过名称查找板块代码
        if name:
            logger.info(f"尝试通过名称查找板块代码: {name}")
            all_boards = await self.get_concept_boards()
            
            # 查找匹配的板块
            for board in all_boards:
                if board.name == name:
                    board_code = board.code
                    logger.info(f"找到板块代码: {board_code}")
                    break
        
        # 获取所有概念板块
        all_boards = await self.get_concept_boards()
        
        # 查找匹配的板块
        for board in all_boards:
            if board.code == board_code:
                return board
        
        logger.warning(f"未找到板块代码 {board_code} 的数据")
        return None
    
    @cache_result()
    @handle_akshare_exception
    @cache_result()
    @handle_akshare_exception
    async def get_concept_board_spot(self, board_name: str) -> Optional[ConceptBoardSpot]:
        """
        获取概念板块实时行情详情
        
        Args:
            board_name: 板块名称，如"可燃冰"
            
        Returns:
            Optional[ConceptBoardSpot]: 概念板块实时行情详情，如果未找到则返回None
        """
        logger.info(f"获取概念板块实时行情详情: {board_name}")
        
        try:
            # 调用AKShare接口获取概念板块实时行情
            df = ak.stock_board_concept_spot_em(symbol=board_name)
            
            if df.empty:
                logger.warning(f"未找到板块名称 {board_name} 的实时行情数据")
                return None
            
            # 将DataFrame转换为字典
            data_dict = {}
            for _, row in df.iterrows():
                data_dict[row["item"]] = row["value"]
            
            # 创建ConceptBoardSpot对象，使用safe_float处理所有浮点值
            spot = ConceptBoardSpot(
                name=board_name,
                price=safe_float(data_dict.get("最新", 0), 0),
                high=safe_float(data_dict.get("最高", 0), 0),
                low=safe_float(data_dict.get("最低", 0), 0),
                open=safe_float(data_dict.get("开盘", 0), 0),
                volume=safe_float(data_dict.get("成交量", 0), 0),
                amount=safe_float(data_dict.get("成交额", 0), 0),
                turnover_rate=safe_float(data_dict.get("换手率", 0), 0),
                change=safe_float(data_dict.get("涨跌额", 0), 0),
                change_percent=safe_float(data_dict.get("涨跌幅", 0), 0),
                amplitude=safe_float(data_dict.get("振幅", 0), 0),
                update_time=datetime.now()
            )
            
            return spot
        except Exception as e:
            logger.error(f"获取概念板块实时行情详情失败: {str(e)}")
            raise
    
    @cache_result()
    @handle_akshare_exception
    async def get_concept_board_spot_by_code(self, board_code: str) -> Optional[ConceptBoardSpot]:
        """
        通过板块代码获取概念板块实时行情详情
        
        Args:
            board_code: 板块代码，如"BK0818"
            
        Returns:
            Optional[ConceptBoardSpot]: 概念板块实时行情详情，如果未找到则返回None
        """
        logger.info(f"通过代码获取概念板块实时行情详情: {board_code}")
        
        # 先获取板块名称
        board = await self.get_concept_board(board_code)
        if board is None:
            logger.warning(f"未找到板块代码 {board_code} 对应的板块")
            return None
        
        # 通过板块名称获取实时行情
        return await self.get_concept_board_spot(board.name)

    @cache_result()
    @handle_akshare_exception
    async def get_concept_board_constituents(self, symbol: str) -> List[ConceptBoardConstituent]:
        """
        获取概念板块成份股
        
        Args:
            symbol: 板块名称或代码，如"融资融券"或"BK0655"
            
        Returns:
            List[ConceptBoardConstituent]: 概念板块成份股列表
        """
        logger.info(f"获取概念板块成份股: {symbol}")
        
        try:
            # 调用AKShare接口获取概念板块成份股
            df = ak.stock_board_concept_cons_em(symbol=symbol)
            
            if df.empty:
                logger.warning(f"未获取到板块 {symbol} 的成份股数据")
                return []
            
            # 将DataFrame转换为ConceptBoardConstituent对象列表
            result = []
            for _, row in df.iterrows():
                # 使用safe_float函数处理所有浮点值
                constituent = ConceptBoardConstituent(
                    rank=int(row["序号"]),
                    code=row["代码"],
                    name=row["名称"],
                    price=safe_float(row["最新价"], 0),
                    change_percent=safe_float(row["涨跌幅"], 0),
                    change=safe_float(row["涨跌额"], 0),
                    volume=safe_float(row["成交量"], 0),
                    amount=safe_float(row["成交额"], 0),
                    amplitude=safe_float(row["振幅"], 0),
                    high=safe_float(row["最高"], 0),
                    low=safe_float(row["最低"], 0),
                    open=safe_float(row["今开"], 0),
                    pre_close=safe_float(row["昨收"], 0),
                    turnover_rate=safe_float(row["换手率"], 0),
                    pe_ratio=safe_float(row["市盈率-动态"]),
                    pb_ratio=safe_float(row["市净率"]),
                    update_time=datetime.now()
                )
                result.append(constituent)
            
            return result
        except Exception as e:
            logger.error(f"获取概念板块成份股失败: {str(e)}")
            # 重要：这里需要抛出异常，而不是返回None
            raise ValueError(f"获取概念板块成份股失败: {str(e)}")

    @cache_result()
    @handle_akshare_exception
    async def get_industry_boards(self) -> List[IndustryBoard]:
        """
        获取行业板块列表及实时行情
        
        Returns:
            List[IndustryBoard]: 行业板块列表
        """
        logger.info("获取行业板块列表")
        
        # 调用AKShare接口获取行业板块数据
        df = ak.stock_board_industry_name_em()
        
        if df.empty:
            logger.warning("未获取到行业板块数据")
            return []
        
        # 将DataFrame转换为IndustryBoard对象列表
        result = []
        for _, row in df.iterrows():
            # 使用safe_float函数处理所有浮点值
            market_value = int(row["总市值"]) if not pd.isna(row["总市值"]) else None
            
            board = IndustryBoard(
                rank=int(row["排名"]),
                name=row["板块名称"],
                code=row["板块代码"],
                price=safe_float(row["最新价"], 0),
                change=safe_float(row["涨跌额"], 0),
                change_percent=safe_float(row["涨跌幅"], 0),
                market_value=market_value,
                turnover_rate=safe_float(row["换手率"], 0),
                up_count=int(row["上涨家数"]),
                down_count=int(row["下跌家数"]),
                leading_stock=row["领涨股票"],
                leading_stock_change_percent=safe_float(row["领涨股票-涨跌幅"], 0),
                update_time=datetime.now()
            )
            result.append(board)
        
        return result
    
    @cache_result()
    @handle_akshare_exception
    async def get_industry_board(self, board_code: str) -> Optional[IndustryBoard]:
        """
        获取单个行业板块的实时行情
        
        Args:
            board_code: 板块代码，如"BK0437"
            
        Returns:
            Optional[IndustryBoard]: 行业板块数据，如果未找到则返回None
        """
        logger.info(f"获取单个行业板块: {board_code}")
        
        # 获取所有行业板块
        all_boards = await self.get_industry_boards()
        
        # 查找匹配的板块
        for board in all_boards:
            if board.code == board_code:
                return board
        
        logger.warning(f"未找到板块代码 {board_code} 的数据")
        return None

    @cache_result()
    @handle_akshare_exception
    async def get_industry_board_spot(self, board_name: str) -> Optional[IndustryBoardSpot]:
        """
        获取行业板块实时行情详情
        
        Args:
            board_name: 板块名称，如"小金属"
            
        Returns:
            Optional[IndustryBoardSpot]: 行业板块实时行情详情，如果未找到则返回None
        """
        logger.info(f"获取行业板块实时行情详情: {board_name}")
        
        try:
            # 调用AKShare接口获取行业板块实时行情
            df = ak.stock_board_industry_spot_em(symbol=board_name)
            
            if df.empty:
                logger.warning(f"未找到板块名称 {board_name} 的实时行情数据")
                return None
            
            # 将DataFrame转换为字典
            data_dict = {}
            for _, row in df.iterrows():
                data_dict[row["item"]] = row["value"]
            
            # 创建IndustryBoardSpot对象，使用safe_float处理所有浮点值
            spot = IndustryBoardSpot(
                name=board_name,
                price=safe_float(data_dict.get("最新", 0), 0),
                high=safe_float(data_dict.get("最高", 0), 0),
                low=safe_float(data_dict.get("最低", 0), 0),
                open=safe_float(data_dict.get("开盘", 0), 0),
                volume=safe_float(data_dict.get("成交量", 0), 0),
                amount=safe_float(data_dict.get("成交额", 0), 0),
                turnover_rate=safe_float(data_dict.get("换手率", 0), 0),
                change=safe_float(data_dict.get("涨跌额", 0), 0),
                change_percent=safe_float(data_dict.get("涨跌幅", 0), 0),
                amplitude=safe_float(data_dict.get("振幅", 0), 0),
                update_time=datetime.now()
            )
            
            return spot
        except Exception as e:
            logger.error(f"获取行业板块实时行情详情失败: {str(e)}")
            raise
    
    @cache_result()
    @handle_akshare_exception
    async def get_industry_board_spot_by_code(self, board_code: str) -> Optional[IndustryBoardSpot]:
        """
        通过板块代码获取行业板块实时行情详情
        
        Args:
            board_code: 板块代码，如"BK1027"
            
        Returns:
            Optional[IndustryBoardSpot]: 行业板块实时行情详情，如果未找到则返回None
        """
        logger.info(f"通过代码获取行业板块实时行情详情: {board_code}")
        
        # 先获取板块名称
        board = await self.get_industry_board(board_code)
        if board is None:
            logger.warning(f"未找到板块代码 {board_code} 对应的板块")
            return None
        
        # 通过板块名称获取实时行情
        return await self.get_industry_board_spot(board.name)

    @cache_result()
    @handle_akshare_exception
    async def get_industry_board_constituents(self, symbol: str) -> List[IndustryBoardConstituent]:
        """
        获取行业板块成份股
        
        Args:
            symbol: 板块名称或代码，如"小金属"或"BK1027"
            
        Returns:
            List[IndustryBoardConstituent]: 行业板块成份股列表
        """
        logger.info(f"获取行业板块成份股: {symbol}")
        
        try:
            # 调用AKShare接口获取行业板块成份股
            df = ak.stock_board_industry_cons_em(symbol=symbol)
            
            if df.empty:
                logger.warning(f"未获取到板块 {symbol} 的成份股数据")
                return []
            
            # 将DataFrame转换为IndustryBoardConstituent对象列表
            result = []
            for _, row in df.iterrows():
                # 使用safe_float函数处理所有浮点值
                constituent = IndustryBoardConstituent(
                    rank=int(row["序号"]),
                    code=row["代码"],
                    name=row["名称"],
                    price=safe_float(row["最新价"], 0),
                    change_percent=safe_float(row["涨跌幅"], 0),
                    change=safe_float(row["涨跌额"], 0),
                    volume=safe_float(row["成交量"], 0),
                    amount=safe_float(row["成交额"], 0),
                    amplitude=safe_float(row["振幅"], 0),
                    high=safe_float(row["最高"], 0),
                    low=safe_float(row["最低"], 0),
                    open=safe_float(row["今开"], 0),
                    pre_close=safe_float(row["昨收"], 0),
                    turnover_rate=safe_float(row["换手率"], 0),
                    pe_ratio=safe_float(row["市盈率-动态"]),
                    pb_ratio=safe_float(row["市净率"]),
                    update_time=datetime.now()
                )
                result.append(constituent)
            
            return result
        except Exception as e:
            logger.error(f"获取行业板块成份股失败: {str(e)}")