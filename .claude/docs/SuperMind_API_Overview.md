# SuperMind 量化平台 API 文档总览

## 📋 项目概述

本文档库提供了同花顺SuperMind量化平台的完整API文档整理，基于官方帮助文档 https://quant.10jqka.com.cn/view/help 的内容进行结构化整理，方便开发者快速查阅和使用。

## 🎯 文档目标

- ✅ **结构化整理**: 将官方API文档按功能模块重新组织
- ✅ **快速查阅**: 提供多维度索引和快速导航
- ✅ **实用示例**: 包含丰富的代码示例和使用场景
- ✅ **最佳实践**: 总结量化交易中的常见模式和注意事项
- ✅ **本地化存储**: 支持离线查阅，提高开发效率

## 📂 文档架构

```
.claude/docs/
├── SuperMind_API_Overview.md      # 本文件 - 总览和说明
└── APIs/                          # API详细文档目录
    ├── README.md                  # API文档导航和概览
    ├── API_INDEX.md               # 快速查阅索引（重要！）
    ├── backtest_engine/           # 回测引擎专用API
    │   ├── basic_functions.md     # 基本函数框架
    │   ├── trading_functions.md   # 交易相关函数
    │   ├── custom_functions.md    # 自定义运行函数（待完善）
    │   ├── settings_functions.md  # 设置函数（待完善）
    │   ├── data_functions.md      # 数据函数（待完善）
    │   ├── constants.md           # 枚举常量（待完善）
    │   └── important_objects.md   # 重要对象（待完善）
    ├── data_interface/            # 通用数据接口
    │   ├── iwencai_interface.md   # 问财自然语言接口
    │   ├── market_data.md         # 行情资金数据（待完善）
    │   ├── security_info.md       # 证券信息数据（待完善）
    │   └── table_data.md          # 表数据（待完善）
    ├── portfolio_optimizer/       # 组合优化器
    │   └── portfolio_construction.md # 构造组合优化（待完善）
    └── tools/                     # 工具函数
        ├── file_operations.md     # 文件操作工具
        ├── notification.md        # 消息推送（待完善）
        └── utilities.md           # 其他工具函数（待完善）
```

## 🚀 快速开始

### 1. 新手入门路线
如果您是SuperMind新手，建议按以下顺序阅读：

1. **了解平台** → [README.md](APIs/README.md#概述)
2. **搭建第一个策略** → [基本函数框架](APIs/backtest_engine/basic_functions.md)
3. **实现交易逻辑** → [交易函数](APIs/backtest_engine/trading_functions.md)
4. **获取数据** → [问财接口](APIs/data_interface/iwencai_interface.md)

### 2. 快速查阅路线
如果您需要快速查找特定功能：

1. **查找函数** → [API_INDEX.md](APIs/API_INDEX.md) 🔥 **推荐首选**
2. **按功能查找** → [API_INDEX.md - 按用途分类查找](APIs/API_INDEX.md#-按用途分类查找)
3. **查看示例** → 各功能文档中的示例代码

### 3. 高级功能进阶
如果您需要实现复杂功能：

1. **文件存储** → [文件操作](APIs/tools/file_operations.md)
2. **风控设置** → [风险控制](APIs/backtest_engine/trading_functions.md#风险控制)
3. **高级查询** → [问财高级技巧](APIs/data_interface/iwencai_interface.md#高级查询技巧)

## 🔧 SuperMind 平台核心特性

### 策略类型支持
- **股票策略**: 股票、场内基金、可转债
- **股票日内策略**: 日内回转交易
- **期货期权策略**: 期货和期权交易
- **股票期货策略**: 对冲策略
- **场外基金策略**: 基金申赎
- **外汇策略**: 外汇合约交易
- **T+D合约策略**: 延期交收合约

### 核心功能模块

#### 1. 回测引擎
- 提供完整的历史数据回测功能
- 支持多种交易频率（日、分钟、tick）
- 内置风控和成交模拟机制
- 详细的绩效分析报告

#### 2. 数据接口
- **问财接口**: 自然语言查询，极大简化数据获取
- **行情数据**: 实时和历史行情数据
- **基本面数据**: 财务数据和公司信息
- **宏观数据**: 经济指标和资金流向

#### 3. 研究环境
- Python编程环境
- 丰富的数据科学库支持
- 交互式开发和调试
- 结果可视化

#### 4. 实盘交易
- 模拟交易功能
- 仿真交易环境
- 实盘对接（需要申请权限）

## 💡 使用建议

### 开发工作流
1. **策略设计** → 在研究环境中验证思路
2. **参数调优** → 使用回测功能优化参数
3. **风险测试** → 进行压力测试和稳健性分析
4. **模拟验证** → 在模拟环境中验证策略
5. **实盘部署** → 申请实盘权限并部署

### 最佳实践
1. **数据管理**: 使用[文件操作](APIs/tools/file_operations.md)进行数据持久化
2. **风险控制**: 合理设置[滑点](APIs/backtest_engine/trading_functions.md#2-set_slippage---设置滑点)和[手续费](APIs/backtest_engine/trading_functions.md#1-set_commission---设置交易手续费)
3. **性能优化**: 注意[执行效率](APIs/backtest_engine/basic_functions.md#注意事项)
4. **错误处理**: 使用try-catch处理异常情况

### 常见陷阱
1. **init函数重复执行**: 了解[persist机制](APIs/backtest_engine/basic_functions.md#特别说明)
2. **数据获取环境混淆**: 区分[研究环境和回测环境](APIs/data_interface/iwencai_interface.md#接口类型)
3. **函数适用性**: 查看函数[支持矩阵](APIs/backtest_engine/basic_functions.md#函数支持矩阵)
4. **权限限制**: 注意问财接口的[使用限制](APIs/data_interface/iwencai_interface.md#常见问题)

## 📊 文档完成度

### ✅ 已完成
- [x] 基本函数框架文档
- [x] 交易函数详细说明
- [x] 问财接口使用指南
- [x] 文件操作工具函数
- [x] 快速查阅索引
- [x] 项目整体架构

### 🚧 待完善
- [ ] 自定义运行函数（run_daily, run_weekly等）
- [ ] 设置函数详细说明（set_benchmark等）
- [ ] 数据函数完整文档
- [ ] 枚举常量说明
- [ ] 重要对象详解
- [ ] 市场数据接口
- [ ] 证券信息数据
- [ ] 组合优化器
- [ ] 消息推送功能
- [ ] 其他工具函数

## 🤝 贡献指南

如果您在使用过程中发现问题或有改进建议：

1. **内容完善**: 根据官方文档补充缺失的内容
2. **示例优化**: 提供更多实用的代码示例
3. **错误修正**: 发现文档错误请及时修正
4. **最佳实践**: 分享您的使用经验和技巧

## 📞 获取帮助

- **官方文档**: https://quant.10jqka.com.cn/view/help
- **技术支持**: SuperMind@myhexin.com
- **社区交流**: SuperMind官方社区
- **本地SDK**: 需要机构申请权限

---

**文档创建时间**: 2025-10-26
**基于官方文档版本**: 最新版本
**维护者**: Claude Code AI Assistant

*本文档库会根据SuperMind平台API的更新持续维护和完善。*