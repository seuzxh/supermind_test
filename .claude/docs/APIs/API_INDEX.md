# SuperMind API 快速查阅索引

## 📑 文档概览

本文档提供SuperMind平台API的快速索引，帮助您快速找到需要的函数和接口。

## 🚀 快速导航

### 核心函数（最常用）
| 功能分类 | 函数名 | 用途 | 文档位置 |
|---------|--------|------|----------|
| 策略初始化 | `init()` | 策略开始时执行一次 | [basic_functions.md](backtest_engine/basic_functions.md#init) |
| 交易逻辑 | `handle_bar()` | 每个交易频率执行 | [basic_functions.md](backtest_engine/basic_functions.md#handle_bar) |
| 下单交易 | `order()` | 基础下单函数 | [trading_functions.md](backtest_engine/trading_functions.md#1-order) |
| 目标仓位 | `order_target_percent()` | 按比例调整仓位 | [trading_functions.md](backtest_engine/trading_functions.md#2-order_target_percent) |
| 自然语言查询 | `query_iwencai()` | 问财实时数据查询 | [iwencai_interface.md](data_interface/iwencai_interface.md) |
| 文件保存 | `write_file()` | 保存数据到文件 | [file_operations.md](tools/file_operations.md) |

## 📚 完整函数索引

### 回测引擎专用API

#### 基本函数
- `init()` - [初始化函数](backtest_engine/basic_functions.md#1-init---初始化函数)
- `handle_bar()` - [交易频率自动调用函数](backtest_engine/basic_functions.md#2-handle_bar---交易频率自动调用函数)
- `handle_tick()` - [tick行情数据变化时调用](backtest_engine/basic_functions.md#3-handle_tick---tick行情数据变化时调用)
- `open_auction()` - [集合竞价后调用](backtest_engine/basic_functions.md#4-open_auction---集合竞价后调用)
- `before_trading()` - [开盘前调用](backtest_engine/basic_functions.md#5-before_trading---开盘前调用)
- `after_trading()` - [收盘后调用](backtest_engine/basic_functions.md#6-after_trading---收盘后调用)
- `on_order()` - [委托状态更新回调](backtest_engine/basic_functions.md#7-on_order---委托状态更新回调)
- `on_trade()` - [成交回调](backtest_engine/basic_functions.md#8-on_trade---成交回调)

#### 交易函数
- `order()` - [基础下单函数](backtest_engine/trading_functions.md#1-order---基础下单函数)
- `order_target_percent()` - [目标比例下单](backtest_engine/trading_functions.md#2-order_target_percent---目标比例下单)
- `order_target_value()` - [目标金额下单](backtest_engine/trading_functions.md#3-order_target_value---目标金额下单)
- `order_value()` - [按金额下单](backtest_engine/trading_functions.md#4-order_value---按金额下单)

#### 设置函数
- `set_commission()` - [设置交易手续费](backtest_engine/trading_functions.md#1-set_commission---设置交易手续费)
- `set_slippage()` - [设置滑点](backtest_engine/trading_functions.md#2-set_slippage---设置滑点)
- `set_volume_limit()` - [设置最大成交比例](backtest_engine/trading_functions.md#3-set_volume_limit---设置最大成交比例)
- `set_trade_delay()` - [设置下单延迟成交](backtest_engine/trading_functions.md#4-set_trade_delay---设置下单延迟成交)

### 数据接口

#### 问财接口
- `query_iwencai()` - [问财实时数据（研究环境）](data_interface/iwencai_interface.md#1-query_iwencai---问财实时数据研究环境使用)
- `get_iwencai()` - [问财昨日数据（回测环境）](data_interface/iwencai_interface.md#2-get_iwencai---问财昨日数据回测环境使用)

### 工具函数

#### 文件操作
- `write_file()` - [保存文件函数](tools/file_operations.md#1-write_file---保存文件函数)
- `read_file()` - [读取文件函数](tools/file_operations.md#2-read_file---读取文件函数)
- `list_file()` - [查询文件列表](tools/file_operations.md#3-list_file---查询研究环境指定路径下的文件)
- `copy_file()` - [复制/移动文件](tools/file_operations.md#4-copy_file---复制剪贴文件或文件夹)
- `remove_file()` - [删除文件或文件夹](tools/file_operations.md#5-remove_file---删除文件或文件夹)

## 🔍 按用途分类查找

### 🏗️ 策略搭建
如果您正在搭建新策略，请按顺序查看：
1. [基本函数 - init()](backtest_engine/basic_functions.md#1-init---初始化函数)
2. [基本函数 - handle_bar()](backtest_engine/basic_functions.md#2-handle_bar---交易频率自动调用函数)
3. [交易函数 - order()](backtest_engine/trading_functions.md#1-order---基础下单函数)
4. [设置函数 - set_commission()](backtest_engine/trading_functions.md#1-set_commission---设置交易手续费)

### 📊 数据获取
如果需要获取数据：
1. [问财接口概览](data_interface/iwencai_interface.md#概述)
2. [query_iwencai() - 实时数据](data_interface/iwencai_interface.md#1-query_iwencai---问财实时数据研究环境使用)
3. [get_iwencai() - 历史数据](data_interface/iwencai_interface.md#2-get_iwencai---问财昨日数据回测环境使用)
4. [问财语句示例](data_interface/iwencai_interface.md#基础查询示例)

### 💰 交易执行
如果需要实现交易逻辑：
1. [交易函数概览](backtest_engine/trading_functions.md#概述)
2. [基础下单函数](backtest_engine/trading_functions.md#主要交易函数)
3. [订单类型](backtest_engine/trading_functions.md#订单类型-order-style)
4. [回调函数](backtest_engine/trading_functions.md#回调函数)

### 📁 数据管理
如果需要处理文件存储：
1. [文件操作概览](tools/file_operations.md#概述)
2. [write_file() - 保存数据](tools/file_operations.md#1-write_file---保存文件函数)
3. [read_file() - 读取数据](tools/file_operations.md#2-read_file---读取文件函数)
4. [最佳实践](tools/file_operations.md#文件操作最佳实践)

### 🎛️ 风险控制
如果需要设置风控参数：
1. [set_slippage() - 滑点设置](backtest_engine/trading_functions.md#2-set_slippage---设置滑点)
2. [set_volume_limit() - 成交量限制](backtest_engine/trading_functions.md#3-set_volume_limit---设置最大成交比例)
3. [风险控制示例](backtest_engine/trading_functions.md#风险控制)

## 🛠️ 策略模板

### 基础策略模板
```python
from mindgo_api import *

def init(context):
    # 1. 设置基础参数
    # 参考: [设置函数](backtest_engine/trading_functions.md#设置函数)

    # 2. 初始化股票池
    # 参考: [问财接口](data_interface/iwencai_interface.md)

    pass

def handle_bar(context, bar_dict):
    # 1. 获取数据
    # 参考: [问财接口](data_interface/iwencai_interface.md)

    # 2. 执行交易逻辑
    # 参考: [交易函数](backtest_engine/trading_functions.md)

    # 3. 保存中间结果
    # 参考: [文件操作](tools/file_operations.md)

    pass

def after_trading(context):
    # 保存每日结果
    # 参考: [文件操作示例](tools/file_operations.md#3-回测结果保存)
    pass
```

### 高频策略模板
```python
from mindgo_api import *

def init(context):
    # 设置tick级别策略参数
    pass

def handle_tick(context, tick):
    # tick级别交易逻辑
    # 参考: [handle_tick()](backtest_engine/basic_functions.md#3-handle_tick---tick行情数据变化时调用)

    # 高频交易
    # 参考: [交易函数](backtest_engine/trading_functions.md)
    pass
```

## ⚠️ 重要提醒

### 1. 必须引入的包
```python
from mindgo_api import *
```
[参考文档](backtest_engine/basic_functions.md#重要前提)

### 2. 函数适用性
不同策略类型支持的函数不同，请查看[支持矩阵](backtest_engine/basic_functions.md#函数支持矩阵)

### 3. 环境差异
- **研究环境**: 使用`query_iwencai()`获取实时数据
- **回测环境**: 使用`get_iwencai()`获取历史数据
[详细说明](data_interface/iwencai_interface.md#接口类型)

## 🔗 外部链接

- **官方帮助文档**: https://quant.10jqka.com.cn/view/help
- **SuperMind主页**: https://quant.10jqka.com.cn/
- **官方社区**: [SuperMind官方社区](README.md#联系方式)
- **技术支持**: SuperMind@myhexin.com

## 📝 更新日志

- **2025-10-26**: 初始版本创建
- 包含核心API函数文档
- 添加快速查阅索引
- 提供策略模板

---

*提示：建议将此页面加入书签，方便快速查阅所需的API函数。如果找不到需要的函数，请查看[完整文档结构](README.md#文档结构)。*