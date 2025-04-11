from fastapi import APIRouter
from mcp.stock_mcp import StockMCP
from mcp.index_mcp import IndexMCP
from mcp.sector_mcp import SectorMCP
from mcp.sentiment_mcp import SentimentMCP
from mcp.technical_mcp import TechnicalMCP
from mcp.news_mcp import NewsMCP

mcp_router = APIRouter(prefix="/mcp")

# 实例化MCP类
stock_mcp = StockMCP()
index_mcp = IndexMCP()
sector_mcp = SectorMCP()
sentiment_mcp = SentimentMCP()
technical_mcp = TechnicalMCP()
news_mcp = NewsMCP()

# 股票MCP路由
@mcp_router.get("/stock/info/{stock_code}")
async def get_stock_info(stock_code: str):
    return stock_mcp.get_stock_info(stock_code)

@mcp_router.get("/stock/quote/{stock_code}")
async def get_stock_quote(stock_code: str):
    return stock_mcp.get_stock_quote(stock_code)

# 添加其他MCP接口路由...