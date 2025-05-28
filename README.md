# Stock-AKShare 股票数据服务

基于 AKShare 的股票数据服务，提供 FastAPI 和 MCP 双接口模式，为股票分析系统提供稳定、高效的数据支持。

## 设计思想

本项目主要是利用 AKShare 的接口，重新构建 FastAPI 和 MCP 服务，以便为股票分析系统提供完备的数据。主要设计思想如下：

1. **双接口模式**：同时提供 REST API 和 MCP 接口，满足不同场景的需求
   - REST API：适合前端直接调用，提供标准的 HTTP 接口
   - MCP 接口：适合后端服务间调用，提供高性能的 RPC 调用

2. **数据缓存机制**：集成 Redis 缓存，提高数据访问效率
   - 对热点数据进行缓存，减少对 AKShare 的直接调用
   - 通过缓存策略，平衡数据实时性和系统性能

3. **错误处理与稳定性**：
   - 对 AKShare 接口进行封装，统一处理异常情况
   - 将错误尽可能封装在服务内部，减少对调用方的影响
   - 提供优雅的降级和重试机制，提高系统稳定性

4. **模块化设计**：
   - 按业务领域划分模块，如个股信息、指数信息、板块信息等
   - 每个模块独立实现服务层和接口层，便于维护和扩展

5. **统一的数据模型**：
   - 使用 Pydantic 模型定义数据结构，提供类型安全和自动验证
   - 在服务间传递数据时保持一致的数据格式

## 使用方法

### 环境准备

1. 安装依赖：
   ```bash
   poetry install
   ```

2. 配置环境变量（可选）：
   创建 `.env` 文件，配置以下参数：
   ```
   REDIS_URL=redis://localhost:6379/0  # Redis连接地址，用于缓存
   CACHE_ENABLED=true                  # 是否启用缓存
   CACHE_TTL=3600                      # 缓存过期时间（秒）
   LOG_LEVEL=INFO                      # 日志级别
   ```

### 启动服务

1. 启动 FastAPI 服务：
   ```bash
   poetry run python run.py
   ```

2. 服务默认运行在 `http://localhost:8000`，可以通过以下地址访问：
   - API 文档：`http://localhost:8000/docs`
   - MCP 接口：通过 MCP 客户端连接

### API 调用示例

1. REST API 调用：
   ```python
   import requests
   
   # 获取概念板块列表
   response = requests.get("http://localhost:8000/api/v1/sector/concept")
   concept_boards = response.json()
   print(concept_boards)
   ```

2. MCP 接口调用：
   ```python
   from mcp.client import MCPClient
   
   # 创建MCP客户端
   client = MCPClient("localhost", 8000)
   
   # 调用概念板块列表接口
   concept_boards = await client.call("get_concept_boards")
   print(concept_boards)
   ```

3. FastMCP 接口调用（推荐）：
   ```python
   from mcp.client import FastMCPClient
   
   # 创建FastMCP客户端
   client = FastMCPClient("http://localhost:8000")
   
   # 调用概念板块列表接口
   concept_boards = await client.get_concept_boards()
   print(concept_boards)
   ```

## 目录结构

```
stock-akshare/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI主应用
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py            # 配置文件
│   │   └── logging.py           # 日志配置
│   ├── api/
│   │   ├── __init__.py
│   │   ├── endpoints/           # REST API端点
│   │   │   ├── __init__.py
│   │   │   ├── stock.py         # 个股信息API
│   │   │   ├── index.py         # 指数信息API
│   │   │   ├── sector.py        # 板块信息API
│   │   │   ├── sentiment.py     # 市场情绪API
│   │   │   ├── technical.py     # 技术指标API
│   │   │   └── news.py          # 资讯信息API
│   │   └── router.py            # API路由聚合
│   ├── services/                # 业务服务层
│   │   ├── __init__.py
│   │   ├── stock_service.py     # 个股信息服务
│   │   ├── index_service.py     # 指数信息服务
│   │   ├── sector_service.py    # 板块信息服务
│   │   ├── sentiment_service.py # 市场情绪服务
│   │   ├── technical_service.py # 技术指标服务
│   │   └── news_service.py      # 资讯信息服务
│   ├── models/                  # 数据模型
│   │   ├── __init__.py
│   │   ├── stock_models.py      # 个股相关模型
│   │   ├── index_models.py      # 指数相关模型
│   │   ├── sector_models.py     # 板块相关模型
│   │   ├── sentiment_models.py  # 市场情绪相关模型
│   │   ├── technical_models.py  # 技术指标相关模型
│   │   └── news_models.py       # 资讯相关模型
│   ├── utils/                   # 工具函数
│   │   ├── __init__.py
│   │   ├── akshare_wrapper.py   # AKShare接口封装
│   │   ├── cache.py             # 缓存工具
│   │   └── helpers.py           # 辅助函数
│   └── mcp/                     # MCP接口
│       ├── __init__.py
│       ├── router.py            # MCP路由
│       ├── stock_mcp.py         # 个股信息MCP
│       ├── index_mcp.py         # 指数信息MCP
│       ├── sector_mcp.py        # 板块信息MCP
│       ├── sentiment_mcp.py     # 市场情绪MCP
│       ├── technical_mcp.py     # 技术指标MCP
│       └── news_mcp.py          # 资讯信息MCP
├── tests/                       # 测试
│   ├── __init__.py
│   ├── test_api/               # API测试
│   │   ├── __init__.py
│   │   ├── test_stock.py
│   │   └── ...
│   └── test_services/          # 服务测试
│       ├── __init__.py
│       ├── test_stock_service.py
│       └── ...
├── .env                         # 环境变量
├── .gitignore
├── requirements.txt             # 依赖包
├── README.md                    # 项目说明
└── run.py                       # 启动脚本
```

## 升级建议

为了进一步提高开发效率和代码质量，建议考虑使用 FastMCP 来简化 MCP 接口的实现：

```python
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP

app = FastAPI()
mcp = FastMCP(app)

@mcp.method("get_concept_boards")
async def get_concept_boards():
    """获取概念板块列表及实时行情"""
    sector_service = SectorService()
    return await sector_service.get_concept_boards()
```

使用 FastMCP 的主要优势：
1. 代码更简洁，减少重复性工作
2. 更好的类型支持和自动文档生成
3. 统一的错误处理和日志记录
4. 更容易维护和扩展

## 贡献

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 许可

[MIT License](LICENSE)