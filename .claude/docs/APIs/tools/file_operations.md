# 工具函数 - 文件操作

## 概述

SuperMind平台提供了一系列文件操作工具函数，方便在策略中进行数据的持久化存储和读取。

## 1. write_file() - 保存文件函数

### 调用方法
```python
write_file(file_path, content, mode='w')
```

### 参数说明
- `file_path` (str): 文件路径
- `content` (str/dict/list): 要写入的内容
- `mode` (str): 写入模式，默认为'w'（覆盖写入），可追加'a'

### 功能
- 将内容写入指定文件
- 支持文本、JSON等格式
- 自动创建目录（如果不存在）

### 示例
```python
def after_trading(context):
    # 保存当日交易记录
    trades_data = {
        'date': context.trading_dt,
        'trades': context.trades,
        'portfolio_value': context.portfolio.total_value
    }

    write_file('./results/daily_trades.json', trades_data)

def init(context):
    # 保存策略配置
    config = {
        'universe': context.stock,
        'benchmark': context.benchmark,
        'start_date': context.start_date
    }
    write_file('./config/strategy_config.json', config)
```

## 2. read_file() - 读取文件函数

### 调用方法
```python
read_file(file_path, mode='r')
```

### 参数说明
- `file_path` (str): 文件路径
- `mode` (str): 读取模式，默认为'r'

### 返回值
- 文件内容（自动解析JSON格式）

### 示例
```python
def init(context):
    # 读取之前保存的配置
    try:
        config = read_file('./config/strategy_config.json')
        context.stock = config.get('universe', '000001.SZ')
    except FileNotFoundError:
        context.stock = '000001.SZ'  # 默认值

def handle_bar(context, bar_dict):
    # 读取之前计算的指标
    try:
        indicators = read_file('./cache/indicators.json')
        context.ma5 = indicators.get('ma5')
    except:
        # 重新计算
        context.ma5 = calculate_ma5()
```

## 3. list_file() - 查询研究环境指定路径下的文件

### 调用方法
```python
list_file(directory_path)
```

### 参数说明
- `directory_path` (str): 目录路径

### 返回值
- list: 目录下的文件和文件夹列表

### 示例
```python
def init(context):
    # 查看results目录下的文件
    files = list_file('./results')
    log.info(f"Results目录内容: {files}")

    # 查找最新的回测结果文件
    result_files = [f for f in files if f.endswith('.json')]
    if result_files:
        latest_file = sorted(result_files)[-1]
        results = read_file(f'./results/{latest_file}')
        log.info(f"读取最新结果: {latest_file}")
```

## 4. copy_file() - 复制/剪贴文件或文件夹

### 调用方法
```python
copy_file(source_path, target_path, move=False)
```

### 参数说明
- `source_path` (str): 源文件/文件夹路径
- `target_path` (str): 目标路径
- `move` (bool): 是否移动（剪切），默认False（复制）

### 示例
```python
def after_trading(context):
    # 备份当日结果
    current_date = context.trading_dt.strftime('%Y%m%d')
    copy_file('./results', f'./backup/results_{current_date}')

    # 移动临时文件到正式目录
    copy_file('./temp/trades.json', './results/trades.json', move=True)
```

## 5. remove_file() - 删除文件或文件夹

### 调用方法
```python
remove_file(file_path)
```

### 参数说明
- `file_path` (str): 要删除的文件或文件夹路径

### 示例
```python
def init(context):
    # 清理旧的缓存文件
    cache_files = list_file('./cache')
    for file in cache_files:
        if file.endswith('.tmp'):
            remove_file(f'./cache/{file}')

def after_trading(context):
    # 删除过期的临时数据
    if context.trading_dt.weekday() == 4:  # 周五
        remove_file('./temp/weekly_data')
```

## 文件操作最佳实践

### 1. 目录结构建议
```
./
├── config/          # 配置文件
├── data/           # 数据文件
├── results/        # 结果文件
├── cache/          # 缓存文件
├── logs/           # 日志文件
└── backup/         # 备份文件
```

### 2. 错误处理
```python
def safe_file_operation(operation, *args, **kwargs):
    """安全的文件操作包装函数"""
    try:
        return operation(*args, **kwargs)
    except FileNotFoundError:
        log.warning(f"文件不存在: {args[0]}")
        return None
    except PermissionError:
        log.error(f"权限不足: {args[0]}")
        return None
    except Exception as e:
        log.error(f"文件操作失败: {e}")
        return None

# 使用示例
def handle_bar(context, bar_dict):
    data = safe_file_operation(read_file, './data/indicators.json')
    if data is not None:
        context.indicators = data
```

### 3. 文件命名规范
```python
import datetime

def get_filename(prefix, extension='json'):
    """生成规范的文件名"""
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{prefix}_{timestamp}.{extension}"

# 使用示例
def save_results(context, results):
    filename = get_filename('backtest_results')
    write_file(f'./results/{filename}', results)
```

### 4. 数据持久化策略
```python
class DataPersistence:
    def __init__(self, base_path='./data'):
        self.base_path = base_path

    def save_indicators(self, date, indicators):
        """保存指标数据"""
        filename = f"indicators_{date}.json"
        filepath = f"{self.base_path}/{filename}"
        write_file(filepath, indicators)

    def load_indicators(self, date):
        """加载指标数据"""
        filename = f"indicators_{date}.json"
        filepath = f"{self.base_path}/{filename}"
        return read_file(filepath)

    def save_portfolio_state(self, context):
        """保存投资组合状态"""
        state = {
            'date': context.trading_dt,
            'total_value': context.portfolio.total_value,
            'positions': {pos.stock: pos.to_dict()
                         for pos in context.portfolio.positions.values()},
            'cash': context.portfolio.cash
        }
        filename = f"portfolio_{context.trading_dt.strftime('%Y%m%d')}.json"
        write_file(f"{self.base_path}/{filename}", state)
```

## 注意事项

1. **路径权限**: 确保有读写指定路径的权限
2. **存储空间**: 注意文件大小和存储空间限制
3. **并发访问**: 避免多个进程同时写入同一文件
4. **数据备份**: 重要数据建议定期备份
5. **清理机制**: 定期清理过期的临时文件

## 常见使用场景

### 1. 策略参数持久化
```python
def init(context):
    # 保存策略参数
    params = {
        'lookback_period': 20,
        'threshold': 0.02,
        'max_positions': 10
    }
    write_file('./config/strategy_params.json', params)
```

### 2. 中间结果缓存
```python
def calculate_indicators(context):
    cache_file = './cache/indicators.json'

    # 尝试从缓存读取
    try:
        indicators = read_file(cache_file)
        if indicators.get('date') == context.trading_dt:
            return indicators
    except:
        pass

    # 重新计算并缓存
    indicators = compute_indicators()
    indicators['date'] = context.trading_dt
    write_file(cache_file, indicators)

    return indicators
```

### 3. 回测结果保存
```python
def after_trading(context):
    # 保存每日绩效
    daily_performance = {
        'date': context.trading_dt,
        'returns': context.portfolio.returns,
        'alpha': context.portfolio.alpha,
        'beta': context.portfolio.beta,
        'sharpe': context.portfolio.sharpe
    }

    # 追加写入
    filename = './performance/daily_performance.json'
    try:
        existing_data = read_file(filename)
        existing_data.append(daily_performance)
        write_file(filename, existing_data)
    except:
        write_file(filename, [daily_performance])
```

---

*建议：在生产环境中使用文件操作时，要确保有适当的错误处理和备份机制。*