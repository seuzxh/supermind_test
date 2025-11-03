# 回测引擎 - 交易函数

## 概述

交易函数是SuperMind策略中进行买卖操作的核心API，支持多种订单类型和交易模式。

## 主要交易函数

### 1. order() - 基础下单函数

### 调用方法
```python
order(security, amount, style=None, side='long')
```

### 参数说明
- `security` (str): 股票代码，如 '000001.SZ'
- `amount` (int): 委托数量
  - 正数表示买入
  - 负数表示卖出
- `style` (object): 下单类型，默认为市价单
- `side` (str): 多空方向，默认为'long'

### 示例
```python
def handle_bar(context, bar_dict):
    # 买入100股平安银行
    order('000001.SZ', 100)

    # 卖出50股平安银行
    order('000001.SZ', -50)
```

### 2. order_target_percent() - 目标比例下单

### 调用方法
```python
order_target_percent(security, percent)
```

### 参数说明
- `security` (str): 股票代码
- `percent` (float): 目标持仓比例（0-1之间）

### 功能
- 自动计算需要买入或卖出的数量，使该股票持仓达到指定比例

### 示例
```python
def handle_bar(context, bar_dict):
    # 将平安银行持仓比例调整为20%
    order_target_percent('000001.SZ', 0.2)

    # 清仓某只股票
    order_target_percent('000002.SZ', 0)
```

### 3. order_target_value() - 目标金额下单

### 调用方法
```python
order_target_value(security, value)
```

### 参数说明
- `security` (str): 股票代码
- `value` (float): 目标持仓金额

### 示例
```python
def handle_bar(context, bar_dict):
    # 将平安银行持仓金额调整为10000元
    order_target_value('000001.SZ', 10000)
```

### 4. order_value() - 按金额下单

### 调用方法
```python
order_value(security, value)
```

### 参数说明
- `security` (str): 股票代码
- `value` (float): 交易金额（正数买入，负数卖出）

### 示例
```python
def handle_bar(context, bar_dict):
    # 买入价值10000元的平安银行
    order_value('000001.SZ', 10000)
```

## 订单类型 (Order Style)

### 1. 市价单 (MarketOrder)
```python
from mindgo_api import MarketOrder

order('000001.SZ', 100, MarketOrder())
```

### 2. 限价单 (LimitOrder)
```python
from mindgo_api import LimitOrder

# 以15.00元限价买入
order('000001.SZ', 100, LimitOrder(15.00))
```

### 3. 条件单 (StopOrder)
```python
from mindgo_api import StopOrder

# 止损单
order('000001.SZ', -100, StopOrder(14.00))
```

## 回调函数

### 1. on_order() - 委托状态更新回调

### 调用方法
```python
def on_order(context, order):
```

### 参数说明
- `context`: context对象
- `order`: order委托对象，包含委托详情

### 触发时机
- 回测时：下单后立刻触发
- 仿真交易时：会在handle_bar执行完后触发

### 示例
```python
def on_order(context, order):
    if order.status == OrderStatus.filled:
        log.info(f"订单已成交: {order.security}, 数量: {order.filled}")
    elif order.status == OrderStatus.rejected:
        log.warning(f"订单被拒绝: {order.security}, 原因: {order.reason}")
```

### 2. on_trade() - 成交回调

### 调用方法
```python
def on_trade(context, trade):
```

### 参数说明
- `context`: context对象
- `trade`: trade成交对象，包含成交详情

### 触发时机
- 回测时：下单后立刻触发
- 仿真交易时：会在handle_bar执行完后触发

### 示例
```python
def on_trade(context, trade):
    log.info(f"成交记录: {trade.security}, 价格: {trade.price}, 数量: {trade.amount}")

    # 更新持仓信息
    if trade.side == Side.buy:
        log.info(f"买入 {trade.security}, 当前持仓: {context.portfolio.positions[trade.security].total_amount}")
```

## 交易设置函数

### 1. set_commission() - 设置交易手续费

### 调用方法
```python
set_commission(commission)
```

### 参数类型
- **PerOrder**: 按笔收费
- **PerTrade**: 按成交金额收费
- **CustomCommission**: 自定义费率

### 示例
```python
from mindgo_api import PerOrder

def init(context):
    # 按笔收费：买入每笔3元，卖出每笔5元
    set_commission(PerOrder(buy_cost=3, sell_cost=5))

    # 按比例收费
    set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013))
```

### 2. set_slippage() - 设置滑点

### 滑点类型
- **FixedSlippage**: 固定滑点
- **PriceSlippage**: 可变滑点

### 示例
```python
from mindgo_api import FixedSlippage, PriceSlippage

def init(context):
    # 固定滑点：买入价+5，卖出价-5
    set_slippage(FixedSlippage(5))

    # 可变滑点2%：买入价×1.02，卖出价×0.98
    set_slippage(PriceSlippage(0.02))
```

### 3. set_volume_limit() - 设置最大成交比例

### 调用方法
```python
set_volume_limit(daily=None, minute=None)
```

### 参数说明
- `daily` (float): 日级成交量限制比例（0-1）
- `minute` (float): 分钟级成交量限制比例（0-1）

### 示例
```python
def init(context):
    # 日级成交量限制50%，分钟级限制50%
    set_volume_limit(daily=0.5, minute=0.5)

    # 只设置日级限制
    set_volume_limit(daily=0.25)
```

### 4. set_trade_delay() - 设置下单延迟成交

### 调用方法
```python
set_trade_delay(seconds)
```

### 参数说明
- `seconds` (int): 延迟成交时间（秒）

### 示例
```python
def init(context):
    # 设置延迟300秒成交（模拟T+1）
    set_trade_delay(300)
```

## 订单状态监控

### 订单状态枚举
```python
from mindgo_api import OrderStatus

# 常用状态
OrderStatus.new         # 新建订单
OrderStatus.submitted   # 已提交
OrderStatus.cancelled   # 已取消
OrderStatus.partial_filled # 部分成交
OrderStatus.filled      # 完全成交
OrderStatus.rejected    # 被拒绝
```

### 订单管理示例
```python
def handle_bar(context, bar_dict):
    # 检查未成交订单
    for order in context.portfolio.orders:
        if order.status == OrderStatus.submitted:
            log.info(f"等待成交: {order.security}")

        # 取消长时间未成交的订单
        if order.status == OrderStatus.submitted and \
           (context.trading_dt - order.datetime).seconds > 3600:
            cancel_order(order)
```

## 风险控制

### 1. 仓位控制
```python
def handle_bar(context, bar_dict):
    # 单只股票最大仓位不超过20%
    max_position = 0.2

    for stock, position in context.portfolio.positions.items():
        current_ratio = position.total_amount * position.last_price / context.portfolio.total_value
        if current_ratio > max_position:
            # 减仓到目标比例
            order_target_percent(stock, max_position)
```

### 2. 止损止盈
```python
def handle_bar(context, bar_dict):
    for stock, position in context.portfolio.positions.items():
        if position.total_amount > 0:  # 有持仓
            current_price = position.last_price
            cost_price = position.avg_cost

            # 止损：跌幅超过10%
            if current_price < cost_price * 0.9:
                order_target_percent(stock, 0)
                log.info(f"止损卖出: {stock}")

            # 止盈：涨幅超过30%
            elif current_price > cost_price * 1.3:
                order_target_percent(stock, 0)
                log.info(f"止盈卖出: {stock}")
```

## 最佳实践

### 1. 订单管理
```python
class OrderManager:
    def __init__(self):
        self.max_orders_per_day = 100
        self.order_count = 0

    def safe_order(self, security, amount, reason=""):
        """安全的下单函数"""
        if self.order_count >= self.max_orders_per_day:
            log.warning("今日下单次数已达上限")
            return False

        try:
            order(security, amount)
            self.order_count += 1
            log.info(f"下单: {security}, 数量: {amount}, 原因: {reason}")
            return True
        except Exception as e:
            log.error(f"下单失败: {e}")
            return False
```

### 2. 资金管理
```python
def calculate_position_size(context, stock, confidence=0.5):
    """计算仓位大小"""
    total_value = context.portfolio.total_value
    max_single_position = total_value * 0.1  # 单股最大10%

    # 根据信心水平调整仓位
    position_value = max_single_position * confidence

    return position_value / get_current_data()[stock].last_price
```

---

*注意：在实际交易中，请确保设置合理的风控参数，避免过度交易或集中持仓。*