# Update the import statement
from pydantic_settings import BaseSettings
from pydantic import validator

import os
from typing import List, Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "股票分析服务"
    API_V1_STR: str = "/api/v1"
    
    # CORS设置
    ORIGINS: List[str] = ["*"]
    
    # 缓存设置
    CACHE_ENABLED: bool = True
    CACHE_EXPIRATION: int = 300  # 缓存过期时间(秒)
    
    # 日志设置
    LOG_LEVEL: str = "INFO"
    
    # AKShare设置
    AKSHARE_TIMEOUT: float = 60.0  # AKShare接口超时时间(秒)
    
    # Redis缓存设置
    REDIS_ENABLED: bool = True  # 是否启用Redis缓存
    REDIS_HOST: str = "localhost"  # Redis服务器地址
    REDIS_PORT: int = 6379  # Redis服务器端口
    REDIS_DB: int = 0  # Redis数据库索引
    REDIS_PASSWORD: Optional[str] = None  # Redis密码，如果有的话
    REDIS_PREFIX: str = "akshare:"  # Redis键前缀
    REDIS_TIMEOUT: int = 3  # Redis连接超时时间(秒)
    REDIS_CACHE_EXPIRATION: int = 3600  # Redis缓存过期时间(秒)
    
    @validator("REDIS_ENABLED", pre=True)
    def validate_redis_enabled(cls, v, values):
        """根据环境变量自动判断Redis是否可用"""
        if isinstance(v, bool):
            return v
        redis_host = os.getenv("REDIS_HOST", "")
        if redis_host:
            return True
        return False
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()