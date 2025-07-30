import time
import json
import requests
import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional
import logging

class StockMonitor:
    def __init__(self, token: str = None):
        """
        初始化股票监控器
        Args:
            token: 同花顺API token
        """
        self.token = token
        self.base_url = "https://quant.10jqka.com.cn"
        self.session = requests.Session()
        self.previous_prices = {}  # 存储上一次的价格数据用于计算涨速
        
        # 设置日志
        logging.basicConfig(level=logging.INFO, 
                          format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
    
    def get_all_stocks(self) -> List[str]:
        """
        获取所有股票代码列表
        Returns:
            股票代码列表
        """
        try:
            # 根据同花顺API文档获取股票列表
            url = f"{self.base_url}/api/stock/list"
            headers = {
                'Authorization': f'Bearer {self.token}' if self.token else None,
                'Content-Type': 'application/json'
            }
            
            response = self.session.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0:
                    stocks = data.get('data', [])
                    return [stock['code'] for stock in stocks if stock.get('code')]
            
            # 如果API不可用，使用默认的主要股票代码
            self.logger.warning("无法从API获取股票列表，使用默认股票池")
            return self._get_default_stocks()
            
        except Exception as e:
            self.logger.error(f"获取股票列表失败: {e}")
            return self._get_default_stocks()
    
    def _get_default_stocks(self) -> List[str]:
        """
        获取默认的主要股票代码（沪深300成分股等）
        """
        # 这里可以添加主要的股票代码
        return [
            '000001', '000002', '000858', '000895', '000938',
            '600000', '600036', '600519', '600887', '601318',
            '002142', '002415', '002594', '300059', '300750'
        ]
    
    def get_realtime_data(self, stock_codes: List[str]) -> Dict[str, Dict]:
        """
        获取实时行情数据
        Args:
            stock_codes: 股票代码列表
        Returns:
            股票实时数据字典
        """
        try:
            # 分批获取数据，避免单次请求过多
            batch_size = 50
            all_data = {}
            
            for i in range(0, len(stock_codes), batch_size):
                batch_codes = stock_codes[i:i + batch_size]
                batch_data = self._fetch_batch_data(batch_codes)
                all_data.update(batch_data)
                
                # 避免请求过于频繁
                time.sleep(0.1)
            
            return all_data
        
        except Exception as e:
            self.logger.error(f"获取实时数据失败: {e}")
            return {}
    
    def _fetch_batch_data(self, stock_codes: List[str]) -> Dict[str, Dict]:
        """
        批量获取股票数据
        """
        try:
            codes_str = ','.join(stock_codes)
            url = f"{self.base_url}/api/stock/realtime"
            
            params = {
                'codes': codes_str,
                'fields': 'code,name,price,change,change_pct,volume,amount,high,low,open,pre_close'
            }
            
            headers = {
                'Authorization': f'Bearer {self.token}' if self.token else None,
                'Content-Type': 'application/json'
            }
            
            response = self.session.get(url, params=params, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0:
                    stocks_data = data.get('data', [])
                    return {
                        stock['code']: {
                            'name': stock.get('name', ''),
                            'price': float(stock.get('price', 0)),
                            'change': float(stock.get('change', 0)),
                            'change_pct': float(stock.get('change_pct', 0)),
                            'volume': int(stock.get('volume', 0)),
                            'amount': float(stock.get('amount', 0)),
                            'high': float(stock.get('high', 0)),
                            'low': float(stock.get('low', 0)),
                            'open': float(stock.get('open', 0)),
                            'pre_close': float(stock.get('pre_close', 0)),
                            'timestamp': datetime.now()
                        }
                        for stock in stocks_data if stock.get('code')
                    }
            
            # 如果API不可用，返回模拟数据进行测试
            self.logger.warning("API不可用，使用模拟数据")
            return self._generate_mock_data(stock_codes)
            
        except Exception as e:
            self.logger.error(f"批量获取数据失败: {e}")
            return self._generate_mock_data(stock_codes)
    
    def _generate_mock_data(self, stock_codes: List[str]) -> Dict[str, Dict]:
        """
        生成模拟数据用于测试
        """
        import random
        mock_data = {}
        
        for code in stock_codes:
            base_price = random.uniform(10, 100)
            change_pct = random.uniform(-5, 5)
            
            mock_data[code] = {
                'name': f'股票{code}',
                'price': base_price,
                'change': base_price * change_pct / 100,
                'change_pct': change_pct,
                'volume': random.randint(1000000, 100000000),
                'amount': random.uniform(1000000, 1000000000),
                'high': base_price * random.uniform(1.01, 1.05),
                'low': base_price * random.uniform(0.95, 0.99),
                'open': base_price * random.uniform(0.98, 1.02),
                'pre_close': base_price * (100 - change_pct) / 100,
                'timestamp': datetime.now()
            }
        
        return mock_data
    
    def calculate_rise_speed(self, current_data: Dict[str, Dict]) -> Dict[str, float]:
        """
        计算1分钟涨速
        Args:
            current_data: 当前股票数据
        Returns:
            股票代码到涨速的映射
        """
        rise_speeds = {}
        
        for code, data in current_data.items():
            try:
                current_price = data['price']
                current_time = data['timestamp']
                
                if code in self.previous_prices:
                    prev_price = self.previous_prices[code]['price']
                    prev_time = self.previous_prices[code]['timestamp']
                    
                    # 计算时间差（分钟）
                    time_diff = (current_time - prev_time).total_seconds() / 60
                    
                    if time_diff > 0 and prev_price > 0:
                        # 计算每分钟涨幅
                        price_change_pct = ((current_price - prev_price) / prev_price) * 100
                        rise_speed = price_change_pct / time_diff
                        rise_speeds[code] = rise_speed
                    else:
                        rise_speeds[code] = 0
                else:
                    # 首次获取数据，涨速为0
                    rise_speeds[code] = 0
                
                # 更新历史价格数据
                self.previous_prices[code] = {
                    'price': current_price,
                    'timestamp': current_time
                }
                
            except Exception as e:
                self.logger.error(f"计算股票{code}涨速失败: {e}")
                rise_speeds[code] = 0
        
        return rise_speeds
    
    def get_top_rising_stocks(self, stock_data: Dict[str, Dict], 
                             rise_speeds: Dict[str, float], 
                             top_n: int = 100) -> List[Dict]:
        """
        获取涨速前N的股票
        Args:
            stock_data: 股票数据
            rise_speeds: 涨速数据
            top_n: 返回前N个股票
        Returns:
            排序后的股票列表
        """
        try:
            combined_data = []
            
            for code, speed in rise_speeds.items():
                if code in stock_data:
                    data = stock_data[code].copy()
                    data['code'] = code
                    data['rise_speed'] = speed
                    combined_data.append(data)
            
            # 按涨速排序
            sorted_stocks = sorted(combined_data, 
                                 key=lambda x: x['rise_speed'], 
                                 reverse=True)
            
            return sorted_stocks[:top_n]
        
        except Exception as e:
            self.logger.error(f"获取涨速排行失败: {e}")
            return []
    
    def print_top_stocks(self, top_stocks: List[Dict]):
        """
        打印涨速前100股票信息
        """
        if not top_stocks:
            self.logger.warning("没有获取到股票数据")
            return
        
        print(f"\n{'='*80}")
        print(f"{'涨速前100股票':.^76}")
        print(f"{'更新时间: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'):.^76}")
        print(f"{'='*80}")
        
        header = f"{'排名':>4} {'代码':>8} {'名称':<12} {'现价':>8} {'涨跌幅':>8} {'1分钟涨速':>12} {'成交量':>12}"
        print(header)
        print("-" * 80)
        
        for i, stock in enumerate(top_stocks, 1):
            print(f"{i:>4} {stock['code']:>8} {stock['name']:<12} "
                  f"{stock['price']:>8.2f} {stock['change_pct']:>7.2f}% "
                  f"{stock['rise_speed']:>11.2f}% {stock['volume']:>12,}")
    
    def save_to_file(self, top_stocks: List[Dict], filename: str = None):
        """
        保存数据到文件
        """
        if filename is None:
            filename = f"top_rising_stocks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            # 转换datetime对象为字符串以便JSON序列化
            export_data = []
            for stock in top_stocks:
                stock_copy = stock.copy()
                if 'timestamp' in stock_copy:
                    stock_copy['timestamp'] = stock_copy['timestamp'].isoformat()
                export_data.append(stock_copy)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"数据已保存到文件: {filename}")
        
        except Exception as e:
            self.logger.error(f"保存文件失败: {e}")
    
    def run_monitor(self, interval: int = 60, save_results: bool = True):
        """
        运行实时监控
        Args:
            interval: 监控间隔（秒）
            save_results: 是否保存结果到文件
        """
        self.logger.info("开始股票涨速监控...")
        
        try:
            while True:
                start_time = time.time()
                
                # 获取股票列表
                stock_codes = self.get_all_stocks()
                self.logger.info(f"监控股票数量: {len(stock_codes)}")
                
                # 获取实时数据
                current_data = self.get_realtime_data(stock_codes)
                
                if current_data:
                    # 计算涨速
                    rise_speeds = self.calculate_rise_speed(current_data)
                    
                    # 获取前100
                    top_stocks = self.get_top_rising_stocks(current_data, rise_speeds, 100)
                    
                    # 显示结果
                    self.print_top_stocks(top_stocks)
                    
                    # 保存结果
                    if save_results and top_stocks:
                        self.save_to_file(top_stocks)
                
                # 计算休眠时间
                elapsed_time = time.time() - start_time
                sleep_time = max(0, interval - elapsed_time)
                
                if sleep_time > 0:
                    self.logger.info(f"等待{sleep_time:.1f}秒后进行下次监控...")
                    time.sleep(sleep_time)
        
        except KeyboardInterrupt:
            self.logger.info("监控已停止")
        except Exception as e:
            self.logger.error(f"监控过程发生错误: {e}")


def main():
    """
    主函数
    """
    # 初始化监控器
    # 如果有API token，可以在这里设置
    monitor = StockMonitor(token=None)
    
    # 开始监控（每60秒更新一次）
    monitor.run_monitor(interval=60, save_results=True)


if __name__ == "__main__":
    main()