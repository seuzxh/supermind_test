# SuperMind 实用代码示例库

## 📚 目录
1. [基础策略模板](#基础策略模板)
2. [技术指标策略](#技术指标策略)
3. [多因子策略](#多因子策略)
4. [风险管理模块](#风险管理模块)
5. [数据获取工具](#数据获取工具)
6. [绩效分析工具](#绩效分析工具)
7. [实用工具函数](#实用工具函数)

## 基础策略模板

### 1. 经典均线交叉策略

```python
from mindgo_api import *
import numpy as np
import pandas as pd

def init(context):
    # 策略参数设置
    context.stock_pool = ['000001.SZ', '000002.SZ', '600000.SH', '600036.SH']
    context.short_window = 5   # 短期均线窗口
    context.long_window = 20   # 长期均线窗口
    context.max_position = 0.8 # 最大仓位

    # 设置基准和手续费
    set_benchmark('000300.SH')
    set_commission(PerOrder(buy_cost=3, sell_cost=5))
    set_slippage(FixedSlippage(0.01))

def handle_bar(context, bar_dict):
    for stock in context.stock_pool:
        # 获取历史价格
        prices = get_price(stock, context.long_window, 'close')

        if len(prices) < context.long_window:
            continue

        # 计算均线
        ma_short = prices['close'][-context.short_window:].mean()
        ma_long = prices['close'][-context.long_window:].mean()
        current_price = bar_dict[stock].close

        # 当前持仓
        current_position = context.portfolio.positions[stock]

        # 交易逻辑
        if ma_short > ma_long and current_position.total_amount == 0:
            # 金叉买入
            target_value = context.portfolio.total_value * (context.max_position / len(context.stock_pool))
            order_target_value(stock, target_value)
            log.info(f"买入 {stock}, 价格: {current_price}, MA5: {ma_short:.2f}, MA20: {ma_long:.2f}")

        elif ma_short < ma_long and current_position.total_amount > 0:
            # 死叉卖出
            order_target_percent(stock, 0)
            log.info(f"卖出 {stock}, 价格: {current_price}, MA5: {ma_short:.2f}, MA20: {ma_long:.2f}")

def after_trading(context):
    # 记录每日策略状态
    total_value = context.portfolio.total_value
    cash = context.portfolio.cash
    positions_value = total_value - cash

    log.info(f"账户总值: {total_value:.2f}, 现金: {cash:.2f}, 持仓市值: {positions_value:.2f}")
```

### 2. RSI超买超卖策略

```python
from mindgo_api import *
import talib

def init(context):
    context.stock = '000001.SZ'
    context.rsi_period = 14      # RSI周期
    context.rsi_oversold = 30    # 超卖线
    context.rsi_overbought = 70  # 超买线
    context.position_size = 0.5  # 目标仓位

def handle_bar(context, bar_dict):
    # 获取历史价格用于计算RSI
    prices = get_price(context.stock, 50, 'close')

    if len(prices) < context.rsi_period + 5:
        return

    # 计算RSI
    rsi = talib.RSI(prices['close'].values, timeperiod=context.rsi_period)
    current_rsi = rsi[-1]
    current_price = bar_dict[context.stock].close

    # 当前持仓
    current_position = context.portfolio.positions[context.stock]

    # 交易逻辑
    if current_rsi < context.rsi_oversold and current_position.total_amount == 0:
        # RSI超卖，买入
        order_target_percent(context.stock, context.position_size)
        log.info(f"RSI超卖买入 {context.stock}, RSI: {current_rsi:.2f}, 价格: {current_price}")

    elif current_rsi > context.rsi_overbought and current_position.total_amount > 0:
        # RSI超买，卖出
        order_target_percent(context.stock, 0)
        log.info(f"RSI超买卖出 {context.stock}, RSI: {current_rsi:.2f}, 价格: {current_price}")

    # 止损逻辑
    elif current_position.total_amount > 0:
        cost_price = current_position.avg_cost
        if current_price < cost_price * 0.95:  # 5%止损
            order_target_percent(context.stock, 0)
            log.info(f"止损卖出 {context.stock}, 价格: {current_price}, 成本: {cost_price}")
```

## 技术指标策略

### 1. MACD策略

```python
from mindgo_api import *
import talib

def init(context):
    context.stock_pool = query_iwencai("沪深300成分股中市值前50的股票")
    context.fast_period = 12    # 快线周期
    context.slow_period = 26    # 慢线周期
    context.signal_period = 9   # 信号线周期
    context.max_stocks = 10     # 最大持仓数量

def handle_bar(context, bar_dict):
    buy_signals = []
    sell_signals = []

    for stock in context.stock_pool:
        try:
            # 获取价格数据
            prices = get_price(stock, 100, 'close')
            if len(prices) < context.slow_period + context.signal_period:
                continue

            # 计算MACD
            macd, signal, hist = talib.MACD(
                prices['close'].values,
                fastperiod=context.fast_period,
                slowperiod=context.slow_period,
                signalperiod=context.signal_period
            )

            if len(macd) < 2:
                continue

            current_macd = macd[-1]
            current_signal = signal[-1]
            prev_macd = macd[-2]
            prev_signal = signal[-2]

            current_position = context.portfolio.positions[stock]

            # 金叉买入信号
            if prev_macd <= prev_signal and current_macd > current_signal and current_position.total_amount == 0:
                buy_signals.append(stock)

            # 死叉卖出信号
            elif prev_macd >= prev_signal and current_macd < current_signal and current_position.total_amount > 0:
                sell_signals.append(stock)

        except Exception as e:
            log.warning(f"处理股票 {stock} 时出错: {e}")
            continue

    # 执行卖出
    for stock in sell_signals:
        order_target_percent(stock, 0)
        log.info(f"MACD死叉卖出 {stock}")

    # 执行买入（平均分配资金）
    if buy_signals:
        position_size = min(0.8 / len(buy_signals), 0.1)  # 单股最大10%
        for stock in buy_signals:
            order_target_percent(stock, position_size)
            log.info(f"MACD金叉买入 {stock}, 仓位: {position_size:.2%}")
```

### 2. 布林带策略

```python
from mindgo_api import *
import talib

def init(context):
    context.stock = '000001.SZ'
    context.bb_period = 20     # 布林带周期
    context.bb_std = 2         # 标准差倍数
    context.position_size = 0.6

def handle_bar(context, bar_dict):
    # 获取价格数据
    prices = get_price(context.stock, 50, 'close')
    high_prices = get_price(context.stock, 50, 'high')
    low_prices = get_price(context.stock, 50, 'low')

    if len(prices) < context.bb_period:
        return

    # 计算布林带
    upperband, middleband, lowerband = talib.BBANDS(
        prices['close'].values,
        timeperiod=context.bb_period,
        nbdevup=context.bb_std,
        nbdevdn=context.bb_std
    )

    current_price = bar_dict[context.stock].close
    current_upper = upperband[-1]
    current_middle = middleband[-1]
    current_lower = lowerband[-1]

    current_position = context.portfolio.positions[context.stock]

    # 交易逻辑
    if current_price <= current_lower and current_position.total_amount == 0:
        # 价格触及下轨，买入
        order_target_percent(context.stock, context.position_size)
        log.info(f"布林带下轨买入 {context.stock}, 价格: {current_price}, 下轨: {current_lower:.2f}")

    elif current_price >= current_upper and current_position.total_amount > 0:
        # 价格触及上轨，卖出
        order_target_percent(context.stock, 0)
        log.info(f"布林带上轨卖出 {context.stock}, 价格: {current_price}, 上轨: {current_upper:.2f}")

    # 回归中轨止盈
    elif current_position.total_amount > 0 and abs(current_price - current_middle) / current_middle < 0.02:
        if current_position.total_amount > 0:
            order_target_percent(context.stock, 0)
            log.info(f"回归中轨止盈 {context.stock}, 价格: {current_price}, 中轨: {current_middle:.2f}")
```

## 多因子策略

### 1. 价值质量选股策略

```python
from mindgo_api import *
import pandas as pd
import numpy as np

def init(context):
    # 选股参数
    context.universe = query_iwencai("沪深300成分股")
    context.pe_limit = 20          # 市盈率上限
    context.pb_limit = 3           # 市净率上限
    context.roe_min = 0.10         # 最小ROE
    context.debt_ratio_max = 0.6   # 最大资产负债率
    context.max_positions = 20     # 最大持仓数量
    context.rebalance_frequency = 'M'  # 月调仓

    # 上次调仓日期
    context.last_rebalance_date = None

def handle_bar(context, bar_dict):
    current_date = context.trading_dt

    # 检查是否需要调仓
    need_rebalance = False
    if context.last_rebalance_date is None:
        need_rebalance = True
    elif current_date.month != context.last_rebalance_date.month:
        need_rebalance = True

    if not need_rebalance:
        return

    # 获取基本面数据
    fundamental_data = get_fundamental(context.universe)

    # 筛选股票
    selected_stocks = []

    for stock in context.universe:
        try:
            # 获取财务指标
            pe = get_fundamental(stock, 'PE_TTM')
            pb = get_fundamental(stock, 'PB')
            roe = get_fundamental(stock, 'ROE')
            debt_ratio = get_fundamental(stock, 'DEBT_TO_ASSETS')

            # 检查数据完整性
            if any(pd.isna([pe, pb, roe, debt_ratio])):
                continue

            # 应用筛选条件
            if (pe < context.pe_limit and
                pb < context.pb_limit and
                roe > context.roe_min and
                debt_ratio < context.debt_ratio_max):

                # 计算综合评分（ROE权重最大）
                score = (roe * 0.5 +
                        (1/pe) * 0.3 +
                        (1/pb) * 0.2)

                selected_stocks.append((stock, score))

        except Exception as e:
            log.warning(f"处理股票 {stock} 基本面数据时出错: {e}")
            continue

    # 按评分排序，选择前N只
    selected_stocks.sort(key=lambda x: x[1], reverse=True)
    target_stocks = [stock for stock, score in selected_stocks[:context.max_positions]]

    # 执行调仓
    current_positions = [pos.stock for pos in context.portfolio.positions.values() if pos.total_amount > 0]

    # 卖出不在目标组合中的股票
    for stock in current_positions:
        if stock not in target_stocks:
            order_target_percent(stock, 0)
            log.info(f"调仓卖出 {stock}")

    # 买入目标股票（等权重）
    if target_stocks:
        weight = 0.9 / len(target_stocks)  # 保留10%现金
        for stock in target_stocks:
            order_target_percent(stock, weight)
            log.info(f"调仓买入 {stock}, 权重: {weight:.2%}")

    # 更新调仓日期
    context.last_rebalance_date = current_date
    log.info(f"完成月度调仓，持仓数量: {len(target_stocks)}")
```

### 2. 动量反转策略

```python
from mindgo_api import *
import pandas as pd

def init(context):
    context.universe = query_iwencai("中证500成分股")
    context.momentum_period = 20   # 动量计算周期
    context.reversal_period = 5    # 反转计算周期
    context.max_positions = 30     # 最大持仓
    context.rebalance_frequency = 'W'  # 周调仓
    context.last_rebalance_date = None

def handle_bar(context, bar_dict):
    current_date = context.trading_dt

    # 检查调仓频率
    need_rebalance = False
    if context.last_rebalance_date is None:
        need_rebalance = True
    elif current_date.isocalendar().week != context.last_rebalance_date.isocalendar().week:
        need_rebalance = True

    if not need_rebalance:
        return

    # 计算动量和反转因子
    stock_scores = []

    for stock in context.universe:
        try:
            # 获取价格数据
            prices = get_price(stock, max(context.momentum_period, context.reversal_period) + 5, 'close')

            if len(prices) < context.momentum_period + 5:
                continue

            # 计算动量因子（过去20日收益率）
            momentum_return = (prices['close'][-1] / prices['close'][-context.momentum_period-1] - 1)

            # 计算反转因子（过去5日收益率）
            reversal_return = (prices['close'][-1] / prices['close'][-context.reversal_period-1] - 1)

            # 计算波动率
            returns = prices['close'].pct_change().dropna()
            volatility = returns[-20:].std() * np.sqrt(252)  # 年化波动率

            # 综合评分：正动量 + 负反转 + 低波动
            score = (momentum_return * 0.4 -
                    reversal_return * 0.3 -
                    volatility * 0.3)

            stock_scores.append((stock, score, momentum_return, reversal_return, volatility))

        except Exception as e:
            continue

    # 按综合评分排序
    stock_scores.sort(key=lambda x: x[1], reverse=True)

    # 选择评分最高的股票
    target_stocks = [stock for stock, score, _, _, _ in stock_scores[:context.max_positions]]

    # 执行调仓
    current_positions = [pos.stock for pos in context.portfolio.positions.values() if pos.total_amount > 0]

    # 卖出不在目标中的股票
    for stock in current_positions:
        if stock not in target_stocks:
            order_target_percent(stock, 0)

    # 买入目标股票
    if target_stocks:
        weight = 0.95 / len(target_stocks)
        for stock in target_stocks:
            order_target_percent(stock, weight)

    context.last_rebalance_date = current_date
    log.info(f"动量反转调仓完成，持仓: {len(target_stocks)}只")
```

## 风险管理模块

### 1. 综合风险控制系统

```python
from mindgo_api import *
import numpy as np

class RiskManager:
    def __init__(self, context):
        self.context = context
        self.max_portfolio_risk = 0.15  # 最大组合风险
        self.max_single_position = 0.1   # 单股最大仓位
        self.max_sector_exposure = 0.3   # 单行业最大暴露
        self.stop_loss_ratio = 0.08      # 止损比例
        self.max_drawdown = 0.12         # 最大回撤限制

    def check_portfolio_risk(self):
        """检查组合整体风险"""
        portfolio = self.context.portfolio

        # 检查总仓位
        total_position = portfolio.positions_value / portfolio.total_value
        if total_position > 0.9:
            log.warning(f"总仓位过高: {total_position:.2%}")
            return False

        # 检查回撤
        if hasattr(portfolio, 'max_drawdown'):
            if portfolio.max_drawdown < -self.max_drawdown:
                log.warning(f"最大回撤超限: {portfolio.max_drawdown:.2%}")
                return False

        return True

    def check_single_position(self, stock):
        """检查单个股票仓位风险"""
        position = self.context.portfolio.positions[stock]
        portfolio = self.context.portfolio

        if position.total_amount == 0:
            return True

        # 检查单股仓位
        position_ratio = (position.total_amount * position.last_price) / portfolio.total_value
        if position_ratio > self.max_single_position:
            log.warning(f"{stock} 仓位过高: {position_ratio:.2%}")
            return False

        # 检查止损
        if position.last_price < position.avg_cost * (1 - self.stop_loss_ratio):
            log.info(f"{stock} 触发止损: 当前价 {position.last_price}, 成本 {position.avg_cost}")
            return False

        return True

    def adjust_positions(self):
        """调整仓位以符合风险要求"""
        portfolio = self.context.portfolio
        total_value = portfolio.total_value

        for stock, position in portfolio.positions.items():
            if position.total_amount == 0:
                continue

            current_ratio = (position.total_amount * position.last_price) / total_value

            if current_ratio > self.max_single_position:
                target_ratio = self.max_single_position
                order_target_percent(stock, target_ratio)
                log.info(f"调整 {stock} 仓位至 {target_ratio:.2%}")

def init(context):
    context.stock_pool = query_iwencai("沪深300成分股中市值前100的股票")
    context.risk_manager = RiskManager(context)
    context.rebalance_frequency = 20  # 20个交易日调仓一次
    context.trading_days_count = 0

def handle_bar(context, bar_dict):
    context.trading_days_count += 1

    # 风险检查
    if not context.risk_manager.check_portfolio_risk():
        log.warning("组合风险过高，暂停交易")
        return

    # 调仓逻辑
    if context.trading_days_count % context.rebalance_frequency == 0:
        execute_rebalance(context, bar_dict)

    # 日常风险控制
    context.risk_manager.adjust_positions()

def execute_rebalance(context, bar_dict):
    """执行调仓逻辑"""
    # 这里可以添加具体的选股和调仓逻辑
    # 示例：等权重配置前10只股票
    target_stocks = context.stock_pool[:10]
    weight = 0.8 / len(target_stocks)

    for stock in target_stocks:
        if context.risk_manager.check_single_position(stock):
            order_target_percent(stock, weight)
```

### 2. 动态止损系统

```python
from mindgo_api import *

class StopLossManager:
    def __init__(self, context):
        self.context = context
        self.fixed_stop_loss = 0.08    # 固定止损比例
        self.trailing_stop_ratio = 0.05 # 移动止损比例
        self.profit_taking_ratio = 0.2  # 止盈比例
        self.max_holding_days = 60      # 最大持仓天数
        self.position_info = {}         # 记录持仓信息

    def update_position_info(self, stock):
        """更新持仓信息"""
        position = self.context.portfolio.positions[stock]
        if position.total_amount > 0:
            if stock not in self.position_info:
                self.position_info[stock] = {
                    'entry_price': position.avg_cost,
                    'entry_date': self.context.trading_dt,
                    'highest_price': position.last_price,
                    'holding_days': 0
                }
            else:
                # 更新最高价
                if position.last_price > self.position_info[stock]['highest_price']:
                    self.position_info[stock]['highest_price'] = position.last_price

                # 更新持仓天数
                self.position_info[stock]['holding_days'] += 1
        else:
            # 清理已清仓的股票信息
            if stock in self.position_info:
                del self.position_info[stock]

    def check_stop_conditions(self, stock):
        """检查止损条件"""
        position = self.context.portfolio.positions[stock]
        if position.total_amount == 0 or stock not in self.position_info:
            return None

        current_price = position.last_price
        entry_price = self.position_info[stock]['entry_price']
        highest_price = self.position_info[stock]['highest_price']
        holding_days = self.position_info[stock]['holding_days']

        # 1. 固定止损
        if current_price < entry_price * (1 - self.fixed_stop_loss):
            return f"固定止损: 当前价 {current_price:.2f}, 成本 {entry_price:.2f}"

        # 2. 移动止损
        if current_price < highest_price * (1 - self.trailing_stop_ratio):
            return f"移动止损: 当前价 {current_price:.2f}, 最高价 {highest_price:.2f}"

        # 3. 止盈
        if current_price > entry_price * (1 + self.profit_taking_ratio):
            return f"止盈: 当前价 {current_price:.2f}, 成本 {entry_price:.2f}"

        # 4. 时间止损
        if holding_days > self.max_holding_days:
            return f"时间止损: 持仓 {holding_days} 天"

        return None

def init(context):
    context.stock_pool = ['000001.SZ', '000002.SZ', '600000.SH', '600036.SH']
    context.stop_loss_manager = StopLossManager(context)
    context.position_size = 0.2

def handle_bar(context, bar_dict):
    # 更新持仓信息
    for stock in context.stock_pool:
        context.stop_loss_manager.update_position_info(stock)

    # 检查止损条件
    for stock in context.stock_pool:
        stop_reason = context.stop_loss_manager.check_stop_conditions(stock)
        if stop_reason:
            order_target_percent(stock, 0)
            log.info(f"止损卖出 {stock}: {stop_reason}")

    # 正常交易逻辑（示例）
    for stock in context.stock_pool:
        position = context.portfolio.positions[stock]
        if position.total_amount == 0:
            # 这里可以添加买入逻辑
            pass
```

## 数据获取工具

### 1. 综合数据获取工具

```python
from mindgo_api import *
import pandas as pd
from datetime import datetime, timedelta

class DataManager:
    def __init__(self):
        self.cache = {}
        self.cache_expiry = {}

    def get_cached_data(self, key, data_func, expiry_minutes=60):
        """带缓存的数据获取"""
        now = datetime.now()

        # 检查缓存是否过期
        if (key in self.cache and
            key in self.cache_expiry and
            now < self.cache_expiry[key]):
            return self.cache[key]

        # 获取新数据
        data = data_func()

        # 更新缓存
        self.cache[key] = data
        self.cache_expiry[key] = now + timedelta(minutes=expiry_minutes)

        return data

    def get_stock_prices(self, stocks, count=100, fields=['close', 'volume', 'high', 'low']):
        """批量获取股票价格数据"""
        def fetch_data():
            return get_price(stocks, count, fields)

        cache_key = f"prices_{'_'.join(stocks)}_{count}_{'_'.join(fields)}"
        return self.get_cached_data(cache_key, fetch_data, expiry_minutes=5)

    def get_fundamental_data(self, stocks, fields=['PE_TTM', 'PB', 'ROE']):
        """获取基本面数据"""
        fundamental_data = {}

        for stock in stocks:
            try:
                stock_data = {}
                for field in fields:
                    value = get_fundamental(stock, field)
                    stock_data[field] = value

                fundamental_data[stock] = stock_data
            except Exception as e:
                log.warning(f"获取 {stock} 基本面数据失败: {e}")
                continue

        return fundamental_data

    def get_market_sentiment(self, stocks):
        """获取市场情绪指标"""
        sentiment_data = {}

        for stock in stocks:
            try:
                # 获取价格数据计算技术指标
                prices = self.get_stock_prices([stock], 30)
                if stock in prices:
                    price_data = prices[stock]

                    # 计算价格动量
                    momentum = (price_data['close'][-1] / price_data['close'][-5] - 1)

                    # 计算成交量变化
                    volume_ratio = price_data['volume'][-1] / price_data['volume'][-5:].mean()

                    # 计算价格波动率
                    returns = price_data['close'].pct_change().dropna()
                    volatility = returns[-10:].std()

                    sentiment_data[stock] = {
                        'momentum': momentum,
                        'volume_ratio': volume_ratio,
                        'volatility': volatility
                    }

            except Exception as e:
                log.warning(f"获取 {stock} 情绪数据失败: {e}")
                continue

        return sentiment_data

# 使用示例
data_manager = DataManager()

def init(context):
    context.stock_pool = query_iwencai("沪深300成分股中市值前50的股票")
    context.data_manager = DataManager()

def handle_bar(context, bar_dict):
    # 获取价格数据
    prices = context.data_manager.get_stock_prices(context.stock_pool, 30)

    # 获取基本面数据
    fundamentals = context.data_manager.get_fundamental_data(context.stock_pool)

    # 获取市场情绪数据
    sentiment = context.data_manager.get_market_sentiment(context.stock_pool)

    # 结合多维度数据进行交易决策
    for stock in context.stock_pool:
        if (stock in prices and
            stock in fundamentals and
            stock in sentiment):

            # 这里可以添加基于多维度数据的交易逻辑
            pe = fundamentals[stock].get('PE_TTM', 999)
            momentum = sentiment[stock].get('momentum', 0)

            # 示例：低PE + 正动量
            if pe < 20 and momentum > 0.02:
                current_position = context.portfolio.positions[stock]
                if current_position.total_amount == 0:
                    order_target_percent(stock, 0.05)
                    log.info(f"基于多因子买入 {stock}, PE: {pe:.2f}, 动量: {momentum:.2%}")
```

### 2. 问财数据获取工具

```python
from mindgo_api import *
import time

class WencaiDataLoader:
    def __init__(self):
        self.query_delay = 1  # 查询间隔（秒）
        self.last_query_time = 0

    def safe_wencai_query(self, query, max_retries=3):
        """安全的问财查询"""
        # 控制查询频率
        current_time = time.time()
        if current_time - self.last_query_time < self.query_delay:
            time.sleep(self.query_delay - (current_time - self.last_query_time))

        for attempt in range(max_retries):
            try:
                result = query_iwencai(query)
                self.last_query_time = time.time()
                return result
            except Exception as e:
                if attempt == max_retries - 1:
                    log.error(f"问财查询失败: {query}, 错误: {e}")
                    return None
                else:
                    log.warning(f"问财查询重试 {attempt + 1}/{max_retries}: {query}")
                    time.sleep(2)

        return None

    def get_value_stocks(self, pe_limit=20, pb_limit=3, market_cap_min=50):
        """获取价值型股票"""
        query = f"市盈率小于{pe_limit}且市净率小于{pb_limit}且市值大于{market_cap_min}亿的非ST股票"
        return self.safe_wencai_query(query)

    def get_growth_stocks(self, revenue_growth_min=20, profit_growth_min=15):
        """获取成长型股票"""
        query = f"营收增长率大于{revenue_growth_min}%且净利润增长率大于{profit_growth_min}%的股票"
        return self.safe_wencai_query(query)

    def get_momentum_stocks(self, period=20, min_return=10):
        """获取动量股票"""
        query = f"近{period}日涨幅大于{min_return}%的股票"
        return self.safe_wencai_query(query)

    def get_sector_stocks(self, sector_name):
        """获取特定行业股票"""
        query = f"{sector_name}行业的股票"
        return self.safe_wencai_query(query)

    def get_liquid_stocks(self, min_turnover=1000000):
        """获取高流动性股票"""
        query = f"日成交额大于{min_turnover}元的股票"
        return self.safe_wencai_query(query)

# 使用示例
wencai_loader = WencaiDataLoader()

def init(context):
    context.wencai_loader = WencaiDataLoader()
    context.max_positions = 20
    context.rebalance_day = 1  # 每月1号调仓

def handle_bar(context, bar_dict):
    # 每月调仓
    if context.trading_dt.day == context.rebalance_day:
        # 获取价值股
        value_stocks = context.wencai_loader.get_value_stocks(pe_limit=15, pb_limit=2)

        # 获取成长股
        growth_stocks = context.wencai_loader.get_growth_stocks(revenue_growth_min=25)

        # 获取高流动性股票
        liquid_stocks = context.wencai_loader.get_liquid_stocks()

        # 合并筛选结果
        all_stocks = set()
        if value_stocks is not None and '代码' in value_stocks.columns:
            all_stocks.update(value_stocks['代码'].tolist())

        if growth_stocks is not None and '代码' in growth_stocks.columns:
            all_stocks.update(growth_stocks['代码'].tolist())

        if liquid_stocks is not None and '代码' in liquid_stocks.columns:
            liquid_set = set(liquid_stocks['代码'].tolist())
            all_stocks = all_stocks.intersection(liquid_set)  # 取交集保证流动性

        # 选择目标股票
        target_stocks = list(all_stocks)[:context.max_positions]

        # 执行调仓
        current_positions = [pos.stock for pos in context.portfolio.positions.values() if pos.total_amount > 0]

        # 卖出不在目标中的股票
        for stock in current_positions:
            if stock not in target_stocks:
                order_target_percent(stock, 0)

        # 买入目标股票
        if target_stocks:
            weight = 0.9 / len(target_stocks)
            for stock in target_stocks:
                order_target_percent(stock, weight)

        log.info(f"问财选股调仓完成，目标持仓: {len(target_stocks)}只")
```

## 绩效分析工具

### 1. 策略绩效分析工具

```python
from mindgo_api import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class PerformanceAnalyzer:
    def __init__(self, context):
        self.context = context
        self.daily_returns = []
        self.benchmark_returns = []
        self.dates = []

    def record_daily_performance(self):
        """记录每日绩效数据"""
        portfolio = self.context.portfolio

        # 记录策略收益率
        if hasattr(portfolio, 'daily_returns'):
            self.daily_returns.append(portfolio.daily_returns)
        else:
            # 如果没有直接提供日收益率，计算累计收益率的变化
            if len(self.daily_returns) > 0:
                prev_value = self.daily_returns[-1] if isinstance(self.daily_returns[-1], float) else 1.0
                current_return = (portfolio.total_value / prev_value - 1)
            else:
                current_return = 0.0
            self.daily_returns.append(current_return)

        # 记录基准收益率（需要根据实际情况获取）
        # 这里简化处理，实际应该获取基准指数的收益率
        benchmark_return = 0.0  # 需要实际获取
        self.benchmark_returns.append(benchmark_return)

        # 记录日期
        self.dates.append(self.context.trading_dt)

    def calculate_performance_metrics(self):
        """计算绩效指标"""
        if len(self.daily_returns) < 2:
            return None

        returns = pd.Series(self.daily_returns)
        benchmark_returns = pd.Series(self.benchmark_returns)

        # 基础指标
        total_return = (1 + returns).prod() - 1
        annual_return = (1 + total_return) ** (252 / len(returns)) - 1
        volatility = returns.std() * np.sqrt(252)

        # 风险调整收益
        sharpe_ratio = annual_return / volatility if volatility > 0 else 0

        # 最大回撤
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min()

        # 相对基准指标
        excess_returns = returns - benchmark_returns
        alpha = excess_returns.mean() * 252
        beta = np.cov(returns, benchmark_returns)[0, 1] / np.var(benchmark_returns) if np.var(benchmark_returns) > 0 else 0
        information_ratio = excess_returns.mean() / excess_returns.std() * np.sqrt(252) if excess_returns.std() > 0 else 0

        # 胜率
        win_rate = (returns > 0).mean()

        return {
            'total_return': total_return,
            'annual_return': annual_return,
            'volatility': volatility,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'alpha': alpha,
            'beta': beta,
            'information_ratio': information_ratio,
            'win_rate': win_rate,
            'total_days': len(returns)
        }

    def plot_performance(self):
        """绘制绩效图表"""
        if len(self.daily_returns) < 2:
            print("数据不足，无法绘制图表")
            return

        returns = pd.Series(self.daily_returns)
        dates = pd.to_datetime(self.dates)

        # 计算累计收益
        cumulative_returns = (1 + returns).cumprod()

        # 创建图表
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

        # 累计收益曲线
        ax1.plot(dates, cumulative_returns, label='策略收益', linewidth=2)
        ax1.set_title('策略累计收益曲线')
        ax1.set_ylabel('累计收益')
        ax1.legend()
        ax1.grid(True)

        # 回撤曲线
        running_max = cumulative_returns.expanding().max()
        drawdown = (cumulative_returns - running_max) / running_max
        ax2.fill_between(dates, drawdown, 0, alpha=0.3, color='red', label='回撤')
        ax2.plot(dates, drawdown, color='red', linewidth=1)
        ax2.set_title('策略回撤曲线')
        ax2.set_ylabel('回撤比例')
        ax2.set_xlabel('日期')
        ax2.legend()
        ax2.grid(True)

        plt.tight_layout()
        plt.show()

    def generate_report(self):
        """生成绩效报告"""
        metrics = self.calculate_performance_metrics()

        if metrics is None:
            print("数据不足，无法生成报告")
            return

        print("=" * 50)
        print("策略绩效分析报告")
        print("=" * 50)
        print(f"回测天数: {metrics['total_days']}")
        print(f"总收益率: {metrics['total_return']:.2%}")
        print(f"年化收益率: {metrics['annual_return']:.2%}")
        print(f"年化波动率: {metrics['volatility']:.2%}")
        print(f"夏普比率: {metrics['sharpe_ratio']:.3f}")
        print(f"最大回撤: {metrics['max_drawdown']:.2%}")
        print(f"Alpha: {metrics['alpha']:.3f}")
        print(f"Beta: {metrics['beta']:.3f}")
        print(f"信息比率: {metrics['information_ratio']:.3f}")
        print(f"胜率: {metrics['win_rate']:.2%}")
        print("=" * 50)

# 使用示例
def init(context):
    context.analyzer = PerformanceAnalyzer(context)
    context.stock = '000001.SZ'

def handle_bar(context, bar_dict):
    # 记录每日绩效
    context.analyzer.record_daily_performance()

    # 策略逻辑
    # ... 交易逻辑 ...

def after_trading(context):
    # 每日收盘后生成报告
    context.analyzer.generate_report()
```

## 实用工具函数

### 1. 通用工具函数库

```python
from mindgo_api import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('SuperMind')

def normalize_stock_code(stock_code):
    """标准化股票代码格式"""
    if not stock_code:
        return stock_code

    stock_code = stock_code.upper()

    # 添加交易所后缀
    if stock_code.startswith('6'):
        return stock_code + '.SH'
    elif stock_code.startswith(('0', '3')):
        return stock_code + '.SZ'
    elif stock_code.startswith('8'):
        return stock_code + '.BJ'

    return stock_code

def is_trading_day(date):
    """判断是否为交易日"""
    try:
        # 尝试获取某只股票的数据来判断是否为交易日
        data = get_price('000001.SZ', 1, 'close', end_date=date)
        return len(data) > 0
    except:
        return False

def get_previous_trading_day(date, days=1):
    """获取前N个交易日"""
    current_date = pd.to_datetime(date)
    trading_days = 0

    while trading_days < days:
        current_date -= timedelta(days=1)
        if is_trading_day(current_date):
            trading_days += 1

    return current_date

def calculate_technical_indicators(prices):
    """计算常用技术指标"""
    if len(prices) < 20:
        return None

    indicators = {}

    # 移动平均线
    indicators['MA5'] = prices['close'].rolling(5).mean()
    indicators['MA10'] = prices['close'].rolling(10).mean()
    indicators['MA20'] = prices['close'].rolling(20).mean()

    # RSI
    delta = prices['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    indicators['RSI'] = 100 - (100 / (1 + rs))

    # 布林带
    MA20 = indicators['MA20']
    std20 = prices['close'].rolling(20).std()
    indicators['BOLL_UPPER'] = MA20 + 2 * std20
    indicators['BOLL_LOWER'] = MA20 - 2 * std20

    # MACD
    exp1 = prices['close'].ewm(span=12).mean()
    exp2 = prices['close'].ewm(span=26).mean()
    indicators['MACD'] = exp1 - exp2
    indicators['MACD_SIGNAL'] = indicators['MACD'].ewm(span=9).mean()
    indicators['MACD_HIST'] = indicators['MACD'] - indicators['MACD_SIGNAL']

    return indicators

def portfolio_performance_summary(portfolio):
    """生成组合绩效摘要"""
    summary = {
        '总资产': portfolio.total_value,
        '现金': portfolio.cash,
        '持仓市值': portfolio.positions_value,
        '总收益率': portfolio.returns,
        '今日收益率': getattr(portfolio, 'daily_returns', 0),
        '持仓数量': len([p for p in portfolio.positions.values() if p.total_amount > 0])
    }

    return summary

def risk_metrics_calculator(returns, benchmark_returns=None):
    """计算风险指标"""
    if len(returns) == 0:
        return {}

    metrics = {}

    # 基础统计
    metrics['总收益率'] = (1 + returns).prod() - 1
    metrics['年化收益率'] = (1 + metrics['总收益率']) ** (252 / len(returns)) - 1
    metrics['波动率'] = returns.std() * np.sqrt(252)
    metrics['夏普比率'] = metrics['年化收益率'] / metrics['波动率'] if metrics['波动率'] > 0 else 0

    # 最大回撤
    cumulative = (1 + returns).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max
    metrics['最大回撤'] = drawdown.min()

    # 胜率等
    metrics['胜率'] = (returns > 0).mean()
    metrics['平均正收益'] = returns[returns > 0].mean() if (returns > 0).any() else 0
    metrics['平均负收益'] = returns[returns < 0].mean() if (returns < 0).any() else 0

    # 与基准比较
    if benchmark_returns is not None and len(benchmark_returns) == len(returns):
        excess_returns = returns - benchmark_returns
        metrics['Alpha'] = excess_returns.mean() * 252
        metrics['信息比率'] = excess_returns.mean() / excess_returns.std() * np.sqrt(252) if excess_returns.std() > 0 else 0

    return metrics

def safe_order_target_percent(stock, target_percent, max_percent=0.1):
    """安全的目标百分比下单函数"""
    if target_percent > max_percent:
        logger.warning(f"{stock} 目标仓位 {target_percent:.2%} 超过最大限制 {max_percent:.2%}，调整为最大限制")
        target_percent = max_percent

    try:
        order_target_percent(stock, target_percent)
        logger.info(f"下单成功: {stock}, 目标仓位: {target_percent:.2%}")
        return True
    except Exception as e:
        logger.error(f"下单失败: {stock}, 错误: {e}")
        return False

def batch_get_fundamental_data(stocks, fields, max_retries=3):
    """批量获取基本面数据"""
    fundamental_data = {}

    for stock in stocks:
        for attempt in range(max_retries):
            try:
                stock_data = {}
                for field in fields:
                    value = get_fundamental(stock, field)
                    stock_data[field] = value
                fundamental_data[stock] = stock_data
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    logger.error(f"获取 {stock} 基本面数据失败: {e}")
                else:
                    logger.warning(f"获取 {stock} 基本面数据重试 {attempt + 1}")

    return fundamental_data

def create_stock_universe(criteria_type='market_cap', **kwargs):
    """创建股票池"""
    if criteria_type == 'market_cap':
        # 按市值选股
        min_cap = kwargs.get('min_cap', 50)  # 最小市值（亿）
        max_cap = kwargs.get('max_cap', 1000)  # 最大市值（亿）
        count = kwargs.get('count', 100)

        query = f"市值大于{min_cap}亿小于{max_cap}亿的非ST股票"
        result = query_iwencai(query)

        if result is not None and '代码' in result.columns:
            return result['代码'].head(count).tolist()

    elif criteria_type == 'industry':
        # 按行业选股
        industry = kwargs.get('industry', '银行')
        query = f"{industry}行业的股票"
        result = query_iwencai(query)

        if result is not None and '代码' in result.columns:
            return result['代码'].tolist()

    elif criteria_type == 'index':
        # 指数成分股
        index_code = kwargs.get('index_code', '000300')
        query = f"{index_code}指数成分股"
        result = query_iwencai(query)

        if result is not None and '代码' in result.columns:
            return result['代码'].tolist()

    return []

def log_strategy_status(context, additional_info=None):
    """记录策略状态"""
    portfolio = context.portfolio
    current_date = context.trading_dt

    status_info = {
        '日期': current_date.strftime('%Y-%m-%d'),
        '总资产': f"{portfolio.total_value:.2f}",
        '现金': f"{portfolio.cash:.2f}",
        '持仓市值': f"{portfolio.positions_value:.2f}",
        '总收益率': f"{portfolio.returns:.2%}",
        '持仓数量': len([p for p in portfolio.positions.values() if p.total_amount > 0])
    }

    if additional_info:
        status_info.update(additional_info)

    logger.info(f"策略状态: {status_info}")

# 使用示例
def init(context):
    context.universe = create_stock_universe('market_cap', min_cap=100, count=50)
    context.analyzer = PerformanceAnalyzer(context)

def handle_bar(context, bar_dict):
    # 记录策略状态
    log_strategy_status(context, {'当前持仓': len(context.universe)})

    # 使用技术指标
    for stock in context.universe[:10]:  # 只处理前10只股票作为示例
        prices = get_price(stock, 30, 'close')
        if len(prices) >= 20:
            indicators = calculate_technical_indicators(prices)
            if indicators and len(indicators['RSI']) > 0:
                current_rsi = indicators['RSI'].iloc[-1]
                if current_rsi < 30:  # 超卖
                    safe_order_target_percent(stock, 0.05)
```

---

**说明**: 以上代码示例仅供参考，实际使用时请根据具体需求进行调整和优化。建议在实盘使用前进行充分的回测验证。

**最后更新**: 2025-10-26
**版本**: v1.0