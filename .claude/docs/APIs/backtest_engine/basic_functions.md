# 回测引擎 - 基本函数

## 概述

基本函数是SuperMind策略框架的核心，构成了策略的生命周期管理。

## 重要前提

```python
# 必须在策略开头引入
from mindgo_api import *
```

## 函数支持矩阵

| 函数名 | 股票 | 股票日内 | 期货期权 | 股票期货 | 场外基金 | 外汇 | T+D合约 |
|--------|------|----------|----------|----------|----------|------|---------|
| init | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| handle_bar | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| handle_tick | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| open_auction | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| before_trading | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| after_trading | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| on_order | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| on_trade | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

## 1. init() - 初始化函数

### 调用方法
```python
def init(context):
```

### 参数说明
- `context`: context对象，用来存放当前账户资金、持仓信息等数据

### 作用
- 初始化函数，进行策略回测与模拟交易时在最开始时执行一次
- 仿真交易在第一次运行策略时执行一次

### 特别说明
- 仅在策略第一次运行时执行
- 在研究环境中，会在`./persist`路径下生成策略同名文件夹用于持久化全局变量
- 如果`./persist`下存在同名路径，则不会执行init

### 重新执行init的方法
1. 删除`./persist`下存在的同名路径
2. 或者更改`research_trade`函数中的策略名称

### 常见报错
```
GlobalVars' object has no attribute '****'
```
- 原因：init执行过后添加了信息，程序无法识别
- 解决：使用上述方法重新执行init

### 用途
- 初始化账户信息
- 设置回测参数
- 定义全局变量
- 设置基准、交易费、滑点、合约池等

### 示例
```python
from mindgo_api import *

def init(context):
    # 设置要交易的标的(平安银行)
    context.stock = '000001.SZ'

    # 设置基准
    set_benchmark('000300.SH')

    # 设置交易费率
    set_commission(PerOrder(buy_cost=0.0003, sell_cost=0.0013))
```

## 2. handle_bar() - 交易频率自动调用函数

### 调用方法
```python
def handle_bar(context, bar_dict):
```

### 参数说明
- `context`: context对象，用来存放当前账户资金、持仓信息等数据
- `bar_dict`: bar_dict对象，用于存放当前订阅所有合约的bar行情数据

### 作用
- 定时执行买卖条件，每个交易频率（日/分钟）自动调用一次

### 注意事项
- 保证代码效率，避免查询大量数据
- 避免执行时间过长，产生延时成本
- 在非交易时间不会触发
- 调用频率根据策略的交易频率确定

### 示例
```python
# 每个交易频率买入100股平安银行
def handle_bar(context, bar_dict):
    order('000001.SZ', 100)

    # 获取当前价格
    current_price = bar_dict['000001.SZ'].close

    # 判断买卖条件
    if current_price > 10:
        # 卖出逻辑
        order_target_percent('000001.SZ', 0.5)
```

## 3. handle_tick() - tick行情数据变化时调用

### 调用方法
```python
def handle_tick(context, tick):
```

### 参数说明
- `context`: context对象，用来存放当前账户资金、持仓信息等数据
- `tick`: tick对象，用于存放当前推送合约的tick行情数据

### 作用
- 当所订阅的股票tick行情数据发生变化时，调用一次

### 注意事项
- 保证代码效率，避免查询大量数据
- 遵循"时间优先，顺序优先"的规则
- 时间戳靠前的股票先执行
- 时间戳相同时按订阅列表顺序执行
- tick行情更新自动触发
- 仅在研究环境的回测接口中支持
- 与handle_bar不能并存

### 示例
```python
def handle_tick(context, tick):
    # 获取tick数据
    symbol = tick.symbol
    current_price = tick.last_price
    volume = tick.volume

    # 基于tick数据的交易逻辑
    if symbol == '000001.SZ' and current_price > 15:
        order(symbol, 100)
```

## 4. open_auction() - 集合竞价后调用

### 调用方法
```python
def open_auction(context):
```

### 作用
- 集合竞价后(9:26)调用一次

### 适用场景
- 仅适用于股票策略
- 用于开盘前的特殊处理逻辑

## 5. before_trading() - 开盘前调用

### 调用方法
```python
def before_trading(context):
```

### 作用
- 开盘前半小时调用一次

### 适用场景
- 盘前数据准备
- 预处理计算
- 设置当日交易参数

### 示例
```python
def before_trading(context):
    # 获取当日日期
    today = context.trading_dt

    # 盘前计算指标
    context.ma5 = get_price('000001.SZ', 5, 'close')['close'].mean()

    # 设置当日交易股票池
    context.stocks = ['000001.SZ', '000002.SZ']
```

## 6. after_trading() - 收盘后调用

### 调用方法
```python
def after_trading(context):
```

### 作用
- 当天收盘后半小时调用一次

### 适用场景
- 盘后数据处理
- 绩效分析
- 日志记录
- 准备次日数据

### 示例
```python
def after_trading(context):
    # 记录当日收益
    daily_return = context.portfolio.returns

    # 保存交易记录
    log.info(f"今日收益率: {daily_return:.2%}")

    # 清理临时数据
    if hasattr(context, 'temp_data'):
        del context.temp_data
```

## 7. on_order() - 委托状态更新回调

### 调用方法
```python
def on_order(context, order):
```

### 参数说明
- `context`: context对象
- `order`: 订单对象

### 作用
- 委托状态更新后的回调函数

### 适用场景
- 订单状态监控
- 撤单重试逻辑
- 订单管理

## 8. on_trade() - 成交回调

### 调用方法
```python
def on_trade(context, trade):
```

### 参数说明
- `context`: context对象
- `trade`: 成交对象

### 作用
- 有成交后的回调函数

### 适用场景
- 成交确认
- 风控检查
- 仓位管理

---

*注意：函数的适用性因策略类型而异，请参考支持矩阵选择合适的函数。*