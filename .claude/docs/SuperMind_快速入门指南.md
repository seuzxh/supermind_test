# SuperMind 量化平台快速入门指南

## 🚀 5分钟快速上手

### 第一步：账号准备
1. **下载客户端**: 访问 https://quant.10jqka.com.cn/ 下载SuperMind客户端
2. **注册账号**: 注册同花顺账号（如果还没有）
3. **登录客户端**: 使用账号登录客户端软件

### 第二步：创建第一个策略

#### 简单均线策略示例
```python
from mindgo_api import *

def init(context):
    # 设置要交易的股票
    context.stock = '000001.SZ'  # 平安银行

    # 设置基准
    set_benchmark('000300.SH')

    # 设置交易费率
    set_commission(PerOrder(buy_cost=3, sell_cost=5))

def handle_bar(context, bar_dict):
    # 获取历史价格数据
    prices = get_price(context.stock, 20, 'close')

    # 计算均线
    ma5 = prices['close'][-5:].mean()
    ma20 = prices['close'][-20:].mean()

    current_price = bar_dict[context.stock].close

    # 交易逻辑：金叉买入，死叉卖出
    if ma5 > ma20 and context.portfolio.positions[context.stock].total_amount == 0:
        # 买入（最多占账户80%）
        order_target_percent(context.stock, 0.8)
        log.info(f"买入 {context.stock}，价格：{current_price}")

    elif ma5 < ma20 and context.portfolio.positions[context.stock].total_amount > 0:
        # 卖出
        order_target_percent(context.stock, 0)
        log.info(f"卖出 {context.stock}，价格：{current_price}")
```

### 第三步：运行回测

```python
# 在研究环境中运行回测
research_strategy(
    code=strategy_code,  # 上面编写的策略代码
    start_date='2022-01-01',
    end_date='2023-12-31',
    frequency='day',
    benchmark='000300.SH',
    initial_cash=1000000
)
```

## 📚 功能模块导航

### 1. 策略研究 - 核心开发环境
**访问路径**: 首页 → 我的策略 → 策略研究

**主要用途**:
- ✅ 策略开发和代码编写
- ✅ 历史数据回测
- ✅ 数据分析和可视化
- ✅ 策略调试和优化

**操作步骤**:
1. 点击"策略研究"进入开发环境
2. 创建新的Python文件
3. 编写策略代码
4. 点击运行按钮执行回测

### 2. 绩效分析 - 结果分析工具
**访问路径**: 首页 → 我的策略 → 绩效分析

**主要用途**:
- 📊 查看策略回测结果
- 📈 分析收益率和风险指标
- 🔍 交易行为分析
- 📋 生成详细报告

**关键指标解读**:
- **总收益率**: 策略总体盈利情况
- **年化收益率**: 年化后的收益率
- **夏普比率**: 风险调整后收益（越高越好）
- **最大回撤**: 最大亏损幅度（越低越好）
- **胜率**: 盈利交易占比

### 3. 指标策略 - 技术分析专用
**访问路径**: 首页 → 我的策略 → 指标策略

**主要用途**:
- 📊 技术指标计算和测试
- 🎯 参数优化
- 📈 信号生成验证
- 🔬 指标有效性分析

**常用技术指标**:
- **MA/EMA**: 移动平均线
- **MACD**: 指数平滑异同移动平均线
- **RSI**: 相对强弱指数
- **BOLL**: 布林带
- **KDJ**: 随机指标

### 4. 因子策略 - 量化因子研究
**访问路径**: 首页 → 我的策略 → 因子策略

**主要用途**:
- 🔍 因子挖掘和分析
- 📊 多因子模型构建
- 🎯 因子有效性检验
- 💡 策略因子化

**常见因子类型**:
- **价值因子**: PE、PB、PS等
- **成长因子**: 营收增长、利润增长等
- **质量因子**: ROE、ROA等
- **技术因子**: 动量、反转等

### 5. 策略监控 - 实盘管理
**访问路径**: 首页 → 我的策略 → 策略监控

**主要用途**:
- 👀 实时策略运行监控
- 📊 绩效实时跟踪
- ⚠️ 异常情况预警
- 📝 交易日志查看

### 6. 策略库 - 策略管理
**访问路径**: 首页 → 我的策略 → 策略库

**主要用途**:
- 💾 策略保存和管理
- 🏷️ 策略分类和标签
- 📖 策略版本控制
- 🌐 社区策略分享

## 🛠️ 开发工具介绍

### 研究环境 (Jupyter Notebook)

**界面布局**:
```
+----------------------------+------------------+
|                            |                  |
|      代码编辑区              |    结果显示区      |
|                            |                  |
|                            |                  |
+----------------------------+------------------+
|          工具栏              |    文件浏览器      |
+----------------------------+------------------+
```

**常用快捷键**:
- `Shift + Enter`: 运行当前单元格
- `Ctrl + Enter`: 运行当前单元格并保持在当前格
- `Alt + Enter`: 运行当前单元格并新建单元格
- `Ctrl + /`: 注释/取消注释
- `Tab`: 代码补全

### 数据获取工具

**基础数据接口**:
```python
# 获取股票价格数据
prices = get_price('000001.SZ', 30, 'close')

# 获取基本面数据
fundamental = get_fundamental('000001.SZ')

# 使用问财自然语言查询
stocks = query_iwencai("市盈率小于20的银行股")
```

**实时数据查询**:
```python
# 获取当前行情数据
current_data = get_current_data()

# 获取账户信息
account_info = context.portfolio

# 获取持仓信息
positions = context.portfolio.positions
```

## 📈 回测系统详解

### 回测参数设置

```python
# 基础回测配置
config = {
    'start_date': '2022-01-01',    # 回测开始日期
    'end_date': '2023-12-31',      # 回测结束日期
    'frequency': 'day',            # 交易频率：'day'/'minute'
    'benchmark': '000300.SH',      # 基准指数
    'initial_cash': 1000000,       # 初始资金
}

# 高级配置
advanced_config = {
    'commission': PerOrder(buy_cost=3, sell_cost=5),  # 手续费
    'slippage': FixedSlippage(0.01),                 # 滑点
    'position_limit': 0.8,                           # 仓位限制
}
```

### 回测结果解读

**收益相关指标**:
- **累计收益**: 策略总收益
- **年化收益**: 年化收益率
- **超额收益**: 相对基准的超额表现
- **alpha**: 策略特有收益
- **beta**: 市场风险暴露

**风险相关指标**:
- **夏普比率**: (年化收益 - 无风险利率) / 年化波动率
- **最大回撤**: 最大损失幅度
- **波动率**: 收益率标准差
- **下行风险**: 亏损波动率

**交易相关指标**:
- **胜率**: 盈利交易次数 / 总交易次数
- **盈亏比**: 平均盈利 / 平均亏损
- **交易频率**: 年交易次数
- **持仓天数**: 平均持仓时间

## 🎯 实盘交易部署

### 一键实盘功能

**前提条件**:
- ✅ 客户端已登录
- ✅ 研究环境正常运行
- ✅ 资金账户已配置

**操作步骤**:
```python
# 1. 初始化交易API
from mindgo_api import TradeAPI, MarketPolicy

trade_api = TradeAPI('资金账号', MarketPolicy())

# 2. 运行实盘策略
research_trade(
    '我的实盘策略',           # 策略名称
    strategy_code,            # 策略代码
    frequency='day',          # 交易频率
    trade_api=trade_api,      # 交易API
    signal_mode=False,        # 信号模式
    recover_dt='today'        # 恢复日期
)
```

### 实盘注意事项

**⚠️ 重要提醒**:
1. **客户端必须保持运行状态**
2. **研究环境需要正常启动**
3. **网络连接必须稳定**
4. **全局变量必须可序列化**

**🔒 风控建议**:
```python
def init(context):
    # 设置风控参数
    context.max_position = 0.6      # 最大仓位60%
    context.max_single = 0.2        # 单股最大20%
    context.stop_loss = 0.08        # 止损8%

def handle_bar(context, bar_dict):
    # 仓位检查
    current_pos = context.portfolio.positions_value / context.portfolio.total_value
    if current_pos > context.max_position:
        log.warning("仓位过高，暂停交易")
        return

    # 执行交易逻辑
    # ... 策略逻辑 ...
```

## 🆘 常见问题解决

### 1. 环境问题

**Q: 研究环境无法启动？**
A:
- 检查网络连接
- 重启客户端
- 清理浏览器缓存
- 联系技术支持

**Q: 代码运行缓慢？**
A:
- 减少循环次数
- 使用向量化操作
- 缓存计算结果
- 优化算法逻辑

### 2. 数据问题

**Q: 无法获取数据？**
A:
- 检查股票代码格式
- 确认数据查询权限
- 检查查询日期范围
- 查看错误日志

**Q: 数据不完整？**
A:
- 检查停牌信息
- 确认股票上市时间
- 使用数据清理函数
- 选择替代数据源

### 3. 交易问题

**Q: 下单失败？**
A:
- 检查账户余额
- 确认交易权限
- 检查股票代码
- 查看错误信息

**Q: 实盘与回测差异大？**
A:
- 考虑交易成本
- 处理滑点影响
- 优化执行逻辑
- 增加容错机制

## 📖 学习路径建议

### 新手入门 (1-2周)
1. **第1-3天**: 熟悉平台界面和基础操作
2. **第4-7天**: 学习基础API和简单策略编写
3. **第8-10天**: 掌握回测系统和结果分析
4. **第11-14天**: 尝试参数优化和策略改进

### 进阶提升 (1-2个月)
1. **第1-2周**: 深入学习数据获取和处理
2. **第3-4周**: 掌握多因子策略开发
3. **第5-6周**: 学习风险管理和资金管理
4. **第7-8周**: 实盘交易和策略监控

### 高级应用 (持续学习)
1. **机器学习**: 算法交易和预测模型
2. **高频交易**: 短周期策略开发
3. **组合优化**: 多策略组合管理
4. **风险建模**: 高级风险管理技术

## 🔗 有用链接

- **官方网站**: https://quant.10jqka.com.cn/
- **帮助文档**: https://quant.10jqka.com.cn/view/help
- **社区论坛**: SuperMind量化社区
- **视频教程**: 官方使用教程合集
- **API文档**: 完整API接口文档

---

📧 **技术支持**: SuperMind@myhexin.com
💬 **社区交流**: SuperMind官方社区
📚 **更多资源**: 查看完整策略开发指南

**最后更新**: 2025-10-26
**版本**: v1.0