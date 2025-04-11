from fastapi import APIRouter

from app.api.endpoints import stock_routes, index, sector, sentiment, technical, news

api_router = APIRouter()

api_router.include_router(stock_routes.router, prefix="/stock", tags=["个股信息"])
api_router.include_router(index.router, prefix="/index", tags=["指数信息"])
api_router.include_router(sector.router, prefix="/sector", tags=["板块信息"])
api_router.include_router(sentiment.router, prefix="/sentiment", tags=["市场情绪"])
api_router.include_router(technical.router, prefix="/technical", tags=["技术指标"])
api_router.include_router(news.router, prefix="/news", tags=["资讯信息"])