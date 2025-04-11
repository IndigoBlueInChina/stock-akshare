d:\workroom\indigoblue\stock-akshare\
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI主应用
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py            # 配置文件
│   │   └── logging.py           # 日志配置
│   ├── api/
│   │   ├── __init__.py
│   │   ├── endpoints/
│   │   │   ├── __init__.py
│   │   │   ├── stock.py         # 个股信息API
│   │   │   ├── index.py         # 指数信息API
│   │   │   ├── sector.py        # 板块信息API
│   │   │   ├── sentiment.py     # 市场情绪API
│   │   │   ├── technical.py     # 技术指标API
│   │   │   └── news.py          # 资讯信息API
│   │   └── router.py            # API路由聚合
│   ├── services/
│   │   ├── __init__.py
│   │   ├── stock_service.py     # 个股信息服务
│   │   ├── index_service.py     # 指数信息服务
│   │   ├── sector_service.py    # 板块信息服务
│   │   ├── sentiment_service.py # 市场情绪服务
│   │   ├── technical_service.py # 技术指标服务
│   │   └── news_service.py      # 资讯信息服务
│   ├── models/
│   │   ├── __init__.py
│   │   ├── stock.py             # 个股相关模型
│   │   ├── index.py             # 指数相关模型
│   │   ├── sector.py            # 板块相关模型
│   │   ├── sentiment.py         # 市场情绪相关模型
│   │   ├── technical.py         # 技术指标相关模型
│   │   └── news.py              # 资讯相关模型
│   └── utils/
│       ├── __init__.py
│       ├── akshare_wrapper.py   # AKShare接口封装
│       └── helpers.py           # 辅助函数
│   ├── mcp/
│   │   ├── __init__.py
│   │   ├── stock_mcp.py             # 个股信息MCP
    │   ├── index_mcp.py             # 指数信息MCP
    │   ├── sector_mcp.py            # 板块信息MCP
    │   ├── sentiment_mcp.py         # 市场情绪MCP
    │   ├── technical_mcp.py         # 技术指标MCP
    │   └── news_mcp.py              # 资讯信息MCP
├── tests/
│   ├── __init__.py
│   ├── test_api/
│   │   ├── __init__.py
│   │   ├── test_stock.py
│   │   └── ...
│   └── test_services/
│       ├── __init__.py
│       ├── test_stock_service.py
│       └── ...
├── .env                         # 环境变量
├── .gitignore
├── requirements.txt
├── README.md
└── run.py                       # 启动脚本