# SuperMind 技术指标策略快速参考

## 🚀 常用技术指标策略一览

### 趋势类指标

| 策略名称 | 核心逻辑 | 关键参数 | 适用场景 | 信号类型 |
|---------|---------|---------|---------|---------|
| **双均线交叉** | 短均线上穿长均线买入 | MA5 vs MA20 | 趋势市场 | 趋势跟踪 |
| **MACD金叉** | DIF上穿DEA买入 | (12,26,9) | 中长期趋势 | 趋势跟踪 |
| **布林带突破** | 价格突破上轨买入 | (20,2) | 突破行情 | 趋势跟踪 |
| **三均线** | 短>中>长时买入 | (5,20,60) | 强趋势确认 | 趋势跟踪 |
| **EMA交叉** | 快EMA上穿慢EMA | (12,26) | 敏感趋势跟踪 | 趋势跟踪 |

### 震荡类指标

| 策略名称 | 核心逻辑 | 关键参数 | 适用场景 | 信号类型 |
|---------|---------|---------|---------|---------|
| **RSI超买超卖** | RSI<30买入，>70卖出 | RSI(14) | 震荡市场 | 均值回归 |
| **KDJ金叉** | K线上穿D线买入 | (9,3,3) | 短期波动 | 震荡指标 |
| **威廉指标** | WR<20超买，>80超卖 | WR(14) | 震荡市场 | 均值回归 |
| **RSI背离** | 价格与RSI背离信号 | RSI(14) | 趋势反转 | 反转信号 |
| **CCI** | CCI>100超买，<-100超卖 | CCI(14) | 震荡市场 | 均值回归 |

### 成交量类指标

| 策略名称 | 核心逻辑 | 关键参数 | 适用场景 | 信号类型 |
|---------|---------|---------|---------|---------|
| **量价配合** | 价涨量增买入 | 量比>1.5 | 确认信号 | 趋势确认 |
| **OBV趋势** | OBV创新高买入 | OBV累计 | 资金流向 | 趋势确认 |
| **量价背离** | 价升量减警惕背离 | 量价对比 | 顶部预警 | 反转信号 |
| **放量突破** | 放量突破阻力买入 | 放量>2倍 | 突破确认 | 趋势确认 |

### volatility类指标

| 策略名称 | 核心逻辑 | 关键参数 | 适用场景 | 信号类型 |
|---------|---------|---------|---------|---------|
| **ATR通道** | 价格±N×ATR通道 | ATR(14) | 波动交易 | 突破交易 |
| **布林带宽度** | 宽度收缩预示突破 | BW=(B上-B下)/B中 | 变盘预警 | 变盘信号 |
| **ATR止损** | 动态止损2×ATR | ATR(14) | 风险管理 | 风控工具 |

## 📊 快速策略模板

### 模板1: 经典双均线策略

```python
from mindgo_api import *

def init(context):
    context.stock_pool = ['000001.SZ', '000002.SZ', '600000.SH']
    context.short_ma = 5
    context.long_ma = 20
    context.max_position = 0.8

def handle_bar(context, bar_dict):
    for stock in context.stock_pool:
        prices = get_price(stock, context.long_ma, 'close')
        if len(prices) < context.long_ma:
            continue

        ma_short = prices['close'][-context.short_ma:].mean()
        ma_long = prices['close'][-context.long_ma:].mean()
        current_pos = context.portfolio.positions[stock]

        # 金叉买入
        if ma_short > ma_long and current_pos.total_amount == 0:
            order_target_percent(stock, context.max_position/len(context.stock_pool))

        # 死叉卖出
        elif ma_short < ma_long and current_pos.total_amount > 0:
            order_target_percent(stock, 0)
```

### 模板2: RSI超买超卖策略

```python
from mindgo_api import *
import talib

def init(context):
    context.stock = '000001.SZ'
    context.rsi_period = 14
    context.rsi_oversold = 30
    context.rsi_overbought = 70
    context.position_size = 0.6

def handle_bar(context, bar_dict):
    prices = get_price(context.stock, 30, 'close')
    if len(prices) < context.rsi_period + 5:
        return

    rsi = talib.RSI(prices['close'].values, timeperiod=context.rsi_period)
    current_rsi = rsi[-1]
    current_pos = context.portfolio.positions[context.stock]

    # 超卖买入
    if current_rsi < context.rsi_oversold and current_pos.total_amount == 0:
        order_target_percent(context.stock, context.position_size)

    # 超买卖出
    elif current_rsi > context.rsi_overbought and current_pos.total_amount > 0:
        order_target_percent(context.stock, 0)
```

### 模板3: MACD策略

```python
from mindgo_api import *
import talib

def init(context):
    context.stock_pool = query_iwencai("沪深300成分股前50")
    context.fast_period = 12
    context.slow_period = 26
    context.signal_period = 9
    context.max_positions = 10

def handle_bar(context, bar_dict):
    buy_signals = []
    sell_signals = []

    for stock in context.stock_pool:
        try:
            prices = get_price(stock, 100, 'close')
            if len(prices) < context.slow_period + context.signal_period:
                continue

            macd, signal, hist = talib.MACD(
                prices['close'].values,
                fastperiod=context.fast_period,
                slowperiod=context.slow_period,
                signalperiod=context.signal_period
            )

            if len(macd) < 2:
                continue

            current_pos = context.portfolio.positions[stock]

            # 金叉买入
            if macd[-2] <= signal[-2] and macd[-1] > signal[-1] and current_pos.total_amount == 0:
                buy_signals.append(stock)

            # 死叉卖出
            elif macd[-2] >= signal[-2] and macd[-1] < signal[-1] and current_pos.total_amount > 0:
                sell_signals.append(stock)

        except Exception as e:
            continue

    # 执行交易
    for stock in sell_signals:
        order_target_percent(stock, 0)

    if buy_signals:
        weight = min(0.8 / len(buy_signals), 0.1)
        for stock in buy_signals:
            order_target_percent(stock, weight)
```

### 模板4: 布林带策略

```python
from mindgo_api import *
import talib

def init(context):
    context.stock = '000001.SZ'
    context.bb_period = 20
    context.bb_std = 2
    context.position_size = 0.6

def handle_bar(context, bar_dict):
    prices = get_price(context.stock, 50, 'close')
    if len(prices) < context.bb_period:
        return

    upperband, middleband, lowerband = talib.BBANDS(
        prices['close'].values,
        timeperiod=context.bb_period,
        nbdevup=context.bb_std,
        nbdevdn=context.bb_std
    )

    current_price = bar_dict[context.stock].close
    current_pos = context.portfolio.positions[context.stock]

    # 触及下轨买入
    if current_price <= lowerband[-1] and current_pos.total_amount == 0:
        order_target_percent(context.stock, context.position_size)

    # 触及上轨或回归中轨卖出
    elif (current_price >= upperband[-1] or
          abs(current_price - middleband[-1]) / middleband[-1] < 0.02) and current_pos.total_amount > 0:
        order_target_percent(context.stock, 0)
```

## 🎯 策略选择决策树

### 第一步：判断市场类型

```
市场趋势判断 →
├── 明显趋势 → 趋势跟踪策略
│   ├── 上升趋势 → 买入信号为主
│   └── 下降趋势 → 卖出信号为主
└── 震荡整理 → 均值回归策略
    ├── 区间震荡 → 超买超卖策略
    └── 宽幅震荡 → 突破策略
```

### 第二步：选择时间周期

```
时间周期选择 →
├── 短线交易 (日内-3天)
│   ├── RSI(5-14)
│   ├── KDJ(9,3,3)
│   └── 成交量突破
├── 中线交易 (1-4周)
│   ├── MACD(12,26,9)
│   ├── 布林带(20,2)
│   └── 双均线(10,30)
└── 长线交易 (1月以上)
    ├── 三均线(5,20,60)
    ├── MACD周线
    └── 趋势线分析
```

### 第三步：风险等级匹配

```
风险承受能力 →
├── 保守型
│   ├── 大市值股票
│   ├── 低波动策略
│   └── 严格止损(5%)
├── 稳健型
│   ├── 中等市值股票
│   ├── 平衡策略
│   └── 适度止损(8%)
└── 激进型
    ├── 小市值股票
    ├── 高收益策略
    └── 灵活止损(12%)
```

## ⚡ 快速参数调优

### 均线类参数优化
```python
# 优化参数范围
ma_short_range = range(3, 15)      # 短期均线: 3-14
ma_long_range = range(15, 61)      # 长期均线: 15-60

# 推荐组合
recommendations = [
    (5, 20),    # 经典组合
    (8, 25),    # 中期组合
    (10, 30),   # 稳健组合
    (3, 15),    # 短线组合
]
```

### RSI参数优化
```python
# 优化参数范围
rsi_period_range = range(7, 25)     # RSI周期: 7-24
oversold_range = range(20, 35)      # 超卖线: 20-34
overbought_range = range(65, 85)    # 超买线: 65-84

# 推荐组合
rsi_recommendations = [
    (14, 30, 70),  # 经典设置
    (12, 25, 75),  # 敏感设置
    (21, 20, 80),  # 严格设置
]
```

### MACD参数优化
```python
# 优化参数范围
fast_range = range(8, 17)          # 快线: 8-16
slow_range = range(20, 31)         # 慢线: 20-30
signal_range = range(6, 13)        # 信号线: 6-12

# 推荐组合
macd_recommendations = [
    (12, 26, 9),   # 经典设置
    (8, 21, 7),    # 敏感设置
    (15, 30, 12),  # 稳健设置
]
```

## 🔧 常见问题快速解决

### Q1: 策略不产生信号怎么办？
**A: 检查以下几点**
- 参数设置是否合理
- 市场环境是否适合策略类型
- 数据是否完整
- 信号判断条件是否过于严格

### Q2: 假信号太多怎么办？
**A: 优化方法**
- 增加信号确认条件
- 延长计算周期
- 增加过滤条件
- 组合多个指标

### Q3: 策略回撤过大怎么办？
**A: 风控措施**
- 设置止损位
- 降低仓位
- 分散投资
- 优化入场时机

### Q4: 不同股票用同一参数效果差怎么办？
**A: 参数调整**
- 根据股票特性调整参数
- 使用个股历史数据优化
- 考虑行业特性
- 动态参数调整

## 📈 性能评估速查

### 优秀策略标准
- ✅ 年化收益率 > 15%
- ✅ 最大回撤 < 20%
- ✅ 夏普比率 > 1.0
- ✅ 胜率 > 55%
- ✅ 盈亏比 > 1.2

### 可接受策略标准
- ✅ 年化收益率 > 8%
- ✅ 最大回撤 < 30%
- ✅ 夏普比率 > 0.5
- ✅ 胜率 > 50%
- ✅ 盈亏比 > 1.0

### 需要改进的信号
- ❌ 年化收益率 < 5%
- ❌ 最大回撤 > 40%
- ❌ 夏普比率 < 0.3
- ❌ 胜率 < 45%
- ❌ 盈亏比 < 0.8

---

**版本**: v1.0
**更新**: 2025-10-26
**用途**: SuperMind技术指标策略快速参考

*提示：本指南提供的是通用性指导，实际使用时请根据具体市场环境和个人风险偏好进行调整。*