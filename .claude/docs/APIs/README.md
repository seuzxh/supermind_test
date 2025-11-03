# SuperMind 平台 API 文档

## 概述

SuperMind 是同花顺旗下的量化交易平台，提供完整的量化策略研发、回测、实盘交易功能。

## 文档结构

### 📁 目录结构
```
.claude/docs/APIs/
├── README.md                    # 本文件 - 总览和索引
├── backtest_engine/             # 回测引擎专用API
│   ├── basic_functions.md       # 基本函数 (init, handle_bar, handle_tick等)
│   ├── custom_functions.md      # 自定义运行函数 (run_daily, run_weekly等)
│   ├── settings_functions.md    # 设置函数 (set_benchmark, set_commission等)
│   ├── data_functions.md        # 数据函数
│   ├── trading_functions.md     # 交易函数
│   ├── constants.md             # 枚举常量
│   └── important_objects.md     # 重要对象
├── data_interface/              # 通用数据接口
│   ├── market_data.md          # 行情资金数据
│   ├── security_info.md        # 证券信息数据
│   ├── table_data.md           # 表数据
│   └── iwencai_interface.md    # 问财接口
├── portfolio_optimizer/         # 组合优化器
│   └── portfolio_construction.md # 构造组合优化
└── tools/                       # 工具函数
    ├── file_operations.md       # 文件操作函数
    ├── notification.md          # 消息推送函数
    └── utilities.md             # 其他工具函数
```

## API 分类概览

### 1. 回测引擎专用API

#### 支持的策略类型：
- **股票API**: 用于股票、场内基金、可转债策略回测
- **股票日内API**: 用于股票日内回转交易策略回测
- **期货期权API**: 用于期货期权策略回测
- **股票期货API**: 用户股票和期货对冲策略的回测
- **场外基金API**: 用于场外基金申赎策略回测
- **外汇API**: 用于回测外汇合约策略
- **T+D合约API**: 用于回测延期交收合约策略

#### 核心函数框架：
```python
from mindgo_api import *

def init(context):
    """初始化函数 - 策略开始时执行一次"""
    pass

def handle_bar(context, bar_dict):
    """交易频率自动调用函数 - 每个交易频率执行一次"""
    pass

def handle_tick(context, tick):
    """tick行情数据变化时调用 - tick数据更新时执行"""
    pass
```

### 2. 通用数据接口

- 行情资金数据查询
- 证券信息数据获取
- 表数据接口
- 问财接口（自然语言查询）

### 3. 组合优化器

- 投资组合构造和优化

### 4. 工具函数

- 文件操作（读写、复制、删除）
- 消息推送
- 股票代码格式转换
- 自选板块管理

## 重要提醒

1. **引入包**: 所有策略都需要先引入 `from mindgo_api import *`
2. **函数适用性**: 不同的API类型支持不同的函数，具体详见各函数说明
3. **研究环境**: 在研究环境中使用某些接口可能有特殊要求

## 联系方式

- **官方社区**: SuperMind官方社区发帖提问交流
- **邮箱**: SuperMind@myhexin.com
- **旧版本文档**: 可在帮助页面查看旧版本文档

---

*最后更新: 2025-10-26*