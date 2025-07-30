#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
股票涨速监控测试脚本
运行此脚本可以快速测试监控程序的功能
"""

from stock_monitor import StockMonitor
import time

def test_monitor():
    """测试监控功能"""
    print("开始测试股票监控程序...")
    
    # 创建监控器实例
    monitor = StockMonitor()
    
    # 测试获取股票列表
    print("1. 测试获取股票列表...")
    stocks = monitor.get_all_stocks()
    print(f"   获取到 {len(stocks)} 只股票")
    
    # 测试获取实时数据
    print("2. 测试获取实时数据...")
    test_stocks = stocks[:10]  # 只测试前10只股票
    data = monitor.get_realtime_data(test_stocks)
    print(f"   获取到 {len(data)} 只股票的实时数据")
    
    # 测试涨速计算
    print("3. 测试涨速计算...")
    rise_speeds = monitor.calculate_rise_speed(data)
    print(f"   计算了 {len(rise_speeds)} 只股票的涨速")
    
    # 等待1分钟后再次获取数据计算涨速
    print("4. 等待60秒后再次测试涨速计算...")
    time.sleep(5)  # 为了测试，只等待5秒
    
    data2 = monitor.get_realtime_data(test_stocks)
    rise_speeds2 = monitor.calculate_rise_speed(data2)
    
    # 获取涨速前5的股票
    top_stocks = monitor.get_top_rising_stocks(data2, rise_speeds2, 5)
    
    print("5. 显示测试结果...")
    monitor.print_top_stocks(top_stocks)
    
    print("\n测试完成！程序运行正常。")
    print("要开始正式监控，请运行: python stock_monitor.py")

if __name__ == "__main__":
    test_monitor()