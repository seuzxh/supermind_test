# 通用数据接口 - 问财接口

## 概述

问财接口是SuperMind平台提供的自然语言查询接口，允许用户使用自然语言描述来获取金融数据。

## 接口类型

### 1. query_iwencai() - 问财实时数据（研究环境使用）

**使用环境**: 研究环境
**特点**: 与网页版问财使用一致，获取实时数据

#### 调用方法
```python
query_iwencai(question)
```

#### 参数说明
- `question` (str): 自然语言查询语句

#### 返回值
- DataFrame: 查询结果数据

#### 示例
```python
# 查询市盈率小于10的银行股
result = query_iwencai("市盈率小于10的银行股")
print(result)

# 查询涨幅前10的股票
result = query_iwencai("今日涨幅前10的股票")
print(result)

# 查询特定行业的技术指标
result = query_iwencai("贵州茅台近30日均线")
print(result)
```

### 2. get_iwencai() - 问财昨日数据（回测环境使用）

**使用环境**: 回测环境
**特点**: 获取历史回测时点的昨日数据

#### 调用方法
```python
get_iwencai(question)
```

#### 参数说明
- `question` (str): 自然语言查询语句

#### 返回值
- DataFrame: 查询结果数据（回测时点的昨日数据）

#### 示例
```python
def handle_bar(context, bar_dict):
    # 在回测中查询昨日数据
    result = get_iwencai("市盈率小于20的股票")

    # 基于查询结果进行交易
    if not result.empty:
        target_stocks = result['代码'].tolist()[:5]  # 取前5只
        for stock in target_stocks:
            order_target_percent(stock, 0.2)
```

## 问财语句使用技巧

### 基础查询示例

#### 股票筛选
```python
# 基本面筛选
query_iwencai("ROE大于15%的股票")
query_iwencai("净利润增长超过20%的公司")
query_iwencai("市值大于100亿小于500亿的股票")

# 技术指标筛选
query_iwencai("MACD金叉的股票")
query_iwencai("RSI低于30的超卖股票")
query_iwencai("均线多头排列的股票")

# 行业板块筛选
query_iwencai("新能源行业的龙头股票")
query_iwencai("银行板块中市净率最低的股票")
query_iwencai("科技股中研发投入占比高的公司")
```

#### 数据查询
```python
# 价格相关
query_iwencai("贵州茅台近一年收盘价")
query_iwencai("沪深300指数本月走势")

# 财务数据
query_iwencai("比亚迪最新财报数据")
query_iwencai("银行股平均市净率")

# 市场数据
query_iwencai("今日北向资金流向")
query_iwencai("融资融券余额变化")
```

### 高级查询技巧

#### 组合条件查询
```python
# 多条件组合
query_iwencai("市盈率小于20且ROE大于15%的股票")
query_iwencai("市值大于100亿且净利润增长超过30%的科技股")

# 时间条件
query_iwencai("近一月涨幅超过20%的股票")
query_iwencai("今年新高的股票数量")

# 排序查询
query_iwencai("按市盈率从低到高排序的银行股")
query_iwencai("成交量最大的前20只股票")
```

#### 统计分析查询
```python
# 统计类查询
query_iwencai("各行业平均市盈率")
query_iwencai涨停股票数量")
query_iwencai("破净股票统计")

# 比较类查询
query_iwencai("茅台和五粮液市盈率对比")
query_iwencai("银行股和科技股收益率比较")
```

## 常见问题

### 1. 问财接口是否支持本地接口调用？

**答案**: 问财接口主要用于研究环境和回测环境，在策略实盘交易中有使用限制。

### 2. 查询语句的最佳实践

#### 建议
- 使用清晰、具体的描述
- 避免过于复杂的查询条件
- 注意查询结果的数据格式
- 考虑查询频率限制

#### 避免的做法
- 使用模糊不清的描述
- 查询条件过于复杂
- 频繁查询相同数据
- 在循环中进行大量查询

### 3. 数据获取限制

- **频率限制**: 注意查询频率，避免过于频繁的请求
- **数据时效**: 研究环境获取实时数据，回测环境获取历史数据
- **结果格式**: 不同查询可能返回不同格式的数据

## 实用案例集合

### 案例1: 价值投资策略
```python
# 寻找低估值的优质股票
value_stocks = query_iwencai("""
    市盈率小于15且市净率小于2
    且ROE大于12%
    且净利润增长大于10%
    的非ST股票
""")
```

### 案例2: 技术分析策略
```python
# 寻找技术面买入信号
technical_signals = query_iwencai("""
    MACD金叉且成交量放大
    且股价上穿60日均线
    的股票
""")
```

### 案例3: 行业轮动策略
```python
# 寻找热门行业龙头
sector_leaders = query_iwencai("""
    各行业中市值最大且涨幅排名前3的股票
""")
```

### 案例4: 事件驱动策略
```python
# 寻找业绩超预期股票
earnings_surprises = query_iwencai("""
    最新净利润增长超过50%且股价上涨的股票
""")
```

## 参考资源

- **官方文档**: [问财接口详细说明](https://quant.10jqka.com.cn/view/help/4)
- **使用技巧**: [市面最全！一文讲透问财语句深度使用技巧（含50个案例）](https://quant.10jqka.com.cn/view/help/4)
- **社区交流**: SuperMind官方社区

---

*提示：建议在使用问财接口前，先在研究环境中测试查询语句的正确性和返回结果格式。*