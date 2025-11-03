from playwright.sync_api import sync_playwright
import time
import os

def advanced_strategy_test():
    """
    高级策略研究测试
    1. 点击"我的策略-策略研究"
    2. 检查页面内容
    3. 如果没有内容 -> 输出登录失败
    4. 如果有内容 -> 点击策略名称进行回测
    5. 查看回测结果
    """

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        context = browser.new_context()
        page = context.new_page()

        try:
            print("=== Advanced Strategy Research Test ===")

            # 首先访问主页
            print("1. Accessing main page...")
            page.goto("https://quant.10jqka.com.cn", timeout=30000)
            page.wait_for_load_state('networkidle')
            print(f"Main page loaded: {page.title()}")

            # 截图保存初始状态
            initial_screenshot = os.path.join(os.getcwd(), 'strategy_initial.png')
            page.screenshot(path=initial_screenshot, full_page=True)
            print(f"Initial page screenshot: {initial_screenshot}")

            # 查找策略研究相关导航
            print("2. Looking for strategy research navigation...")

            strategy_selectors = [
                'text=策略研究',
                'a[href*="study-index"]',
                '[href*="/view/study-index.html"]',
                'a:has-text("策略研究")'
            ]

            strategy_link = None
            for selector in strategy_selectors:
                try:
                    elements = page.locator(selector).all()
                    for element in elements:
                        if element.is_visible():
                            strategy_link = element
                            print(f"Found strategy research link: {selector}")
                            break
                except:
                    continue

            if strategy_link:
                print("3. Clicking on strategy research link...")
                strategy_link.scroll_into_view_if_needed()
                time.sleep(1)

                # 点击前截图
                before_click_screenshot = os.path.join(os.getcwd(), 'strategy_before_click.png')
                page.screenshot(path=before_click_screenshot, full_page=True)
                print(f"Screenshot before click: {before_click_screenshot}")

                # 点击策略研究链接
                strategy_link.click()
                page.wait_for_load_state('networkidle', timeout=15000)

                # 点击后截图
                after_click_screenshot = os.path.join(os.getcwd(), 'strategy_after_click.png')
                page.screenshot(path=after_click_screenshot, full_page=True)
                print(f"Screenshot after click: {after_click_screenshot}")

                print(f"Current URL: {page.url()}")
                print(f"Page title: {page.title()}")

                print("4. Analyzing strategy research page content...")

                # 检查页面内容 - 判断登录状态
                content_analysis = analyze_page_content(page)

                if not content_analysis['has_strategy_content'] and content_analysis['requires_login']:
                    print("\n❌ LOGIN FAILED - No strategy content available, login required")
                    print("Reasons:")
                    for reason in content_analysis['login_indicators']:
                        print(f"  - {reason}")

                elif content_analysis['has_strategy_content']:
                    print("\n✅ STRATEGY CONTENT FOUND - Can access strategy research content")
                    print("Available features:")
                    for feature in content_analysis['strategy_features']:
                        print(f"  - {feature}")

                    # 继续执行回测操作
                    print("\n5. Looking for strategy items to backtest...")

                    strategy_items = find_strategy_items(page)

                    if strategy_items:
                        # 选择第一个策略项目
                        first_strategy = strategy_items[0]
                        strategy_name = get_strategy_name(first_strategy)
                        print(f"Selected strategy: {strategy_name}")

                        # 滚动到策略位置
                        first_strategy.scroll_into_view_if_needed()
                        time.sleep(1)

                        # 点击前截图
                        before_backtest_screenshot = os.path.join(os.getcwd(), 'backtest_before_click.png')
                        page.screenshot(path=before_backtest_screenshot, full_page=True)
                        print(f"Screenshot before backtest click: {before_backtest_screenshot}")

                        # 点击策略
                        print(f"6. Clicking on strategy: {strategy_name}...")
                        try:
                            first_strategy.click()
                            page.wait_for_load_state('networkidle', timeout=10000)

                            # 点击后截图
                            after_backtest_screenshot = os.path.join(os.getcwd(), 'backtest_after_click.png')
                            page.screenshot(path=after_backtest_screenshot, full_page=True)
                            print(f"Screenshot after backtest click: {after_backtest_screenshot}")

                            # 分析回测结果
                            print("\n7. Analyzing backtest results...")
                            backtest_results = analyze_backtest_results(page)

                            if backtest_results['has_results']:
                                print("✅ BACKTEST RESULTS FOUND:")
                                print(f"  - Total strategies tested: {backtest_results['strategy_count']}")
                                if backtest_results['performance_metrics']:
                                    for metric in backtest_results['performance_metrics']:
                                        print(f"  - {metric}")
                                if backtest_results['chart_elements']:
                                    print(f"  - Charts found: {len(backtest_results['chart_elements'])}")
                                if backtest_results['data_tables']:
                                    print(f"  - Data tables found: {len(backtest_results['data_tables'])}")
                            else:
                                print("❌ NO BACKTEST RESULTS FOUND")
                                print("Possible reasons:")
                                for reason in backtest_results['no_result_reasons']:
                                    print(f"  - {reason}")

                        except Exception as e:
                            print(f"❌ Error clicking strategy: {e}")
                            # 尝试其他点击方法
                            try_alternative_click_methods(page, first_strategy)
                    else:
                        print("❌ NO STRATEGY ITEMS FOUND")
                        print("Possible reasons:")
                        for reason in content_analysis['no_content_reasons']:
                            print(f"  - {reason}")

                else:
                    print("\n⚠️ UNCLEAR CONTENT STATUS")
                    print("Page status is unclear - may need further investigation")

                # 保存最终页面状态
                final_screenshot = os.path.join(os.getcwd(), 'strategy_final_advanced.png')
                page.screenshot(path=final_screenshot, full_page=True)
                print(f"\nFinal screenshot: {final_screenshot}")

                # 保存HTML用于调试
                html_path = os.path.join(os.getcwd(), 'strategy_final_advanced.html')
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(page.content())
                print(f"Final HTML: {html_path}")

            else:
                print("❌ STRATEGY RESEARCH LINK NOT FOUND")
                print("Navigation failed - may need to check page structure")

        except Exception as e:
            print(f"\nTest error: {e}")
            import traceback
            traceback.print_exc()

        finally:
            time.sleep(2)
            browser.close()
            print("\n=== Test Completed ===")

def analyze_page_content(page):
    """分析页面内容，判断登录状态和功能可用性"""
    analysis = {
        'has_strategy_content': False,
        'requires_login': False,
        'strategy_features': [],
        'login_indicators': [],
        'no_content_reasons': []
    }

    try:
        # 检查登录相关元素
        login_indicators = [
            'text=登录',
            'text=请登录',
            'text=需要登录',
            'text=登录后查看',
            '.login',
            '[class*="login"]',
            'href*="login"'
        ]

        page_content = page.content().lower()

        for indicator in login_indicators:
            try:
                elements = page.locator(indicator).all() if isinstance(indicator, str) else [indicator]
                visible_elements = [el for el in elements if el.is_visible()]
                if visible_elements:
                    analysis['login_indicators'].append(f"Found: {indicator}")
                    analysis['requires_login'] = True
            except:
                if isinstance(indicator, str) and indicator.lower() in page_content:
                    analysis['login_indicators'].append(f"Text found: {indicator}")
                    analysis['requires_login'] = True

        # 检查策略内容特征
        strategy_features = [
            ('text=策略', 'strategy content'),
            ('text=回测', 'backtest content'),
            ('text=收益率', 'return rate'),
            ('text=夏普', 'sharpe ratio'),
            ('text=创建策略', 'create strategy'),
            ('text=我的策略', 'my strategies'),
            ('table', 'strategy tables'),
            ('.backtest', 'backtest elements'),
            ('.chart', 'chart elements'),
            ('.strategy', 'strategy items')
        ]

        for feature, category in strategy_features:
            try:
                if isinstance(feature, str):
                    elements = page.locator(f'text={feature}').all()
                else:
                    elements = [feature]

                visible_elements = [el for el in elements if hasattr(el, 'is_visible') and el.is_visible()]
                if visible_elements:
                    analysis['strategy_features'].append(f"{feature} ({category})")
                    analysis['has_strategy_content'] = True
            except:
                continue

        # 如果没有找到策略内容，记录可能原因
        if not analysis['has_strategy_content']:
            analysis['no_content_reasons'] = [
                "Page may be loading",
                "Content may require authentication",
                "Navigation may have failed",
                "Page structure may have changed"
            ]

    except Exception as e:
        analysis['no_content_reasons'].append(f"Analysis error: {e}")

    return analysis

def find_strategy_items(page):
    """查找可点击的策略项目"""
    strategy_selectors = [
        'table tr:has-text)',
        '.strategy-item',
        '.backtest-item',
        '[class*="strategy"]',
        '[onclick*="backtest"]',
        '[onclick*="strategy"]',
        'button:has-text("回测")',
        'a:has-text("详情")',
        '.row-item',
        '[data-strategy]'
    ]

    strategy_items = []
    for selector in strategy_selectors:
        try:
            elements = page.locator(selector).all()
            visible_elements = [el for el in elements if el.is_visible()]
            if visible_elements:
                strategy_items.extend(visible_elements)
                print(f"Found {len(visible_elements)} strategy items with selector: {selector}")
        except:
            continue

    return strategy_items

def get_strategy_name(element):
    """获取策略名称"""
    try:
        # 尝试多种方式获取策略名称
        name_selectors = [
            'text',
            '.name',
            '.title',
            'td:first-child',
            '[data-name]',
            'alt'
        ]

        for selector in name_selectors:
            try:
                if selector == 'text':
                    name = element.inner_text().strip()
                else:
                    name_element = element.locator(selector).first if ':' in selector else element
                    name = name_element.inner_text().strip() if name_element.is_visible() else ""

                if name and len(name) > 0 and len(name) < 100:  # 合理的名称长度
                    return name[:50]  # 限制长度
            except:
                continue

        return "Unknown Strategy"
    except:
        return "Unknown Strategy"

def analyze_backtest_results(page):
    """分析回测结果"""
    results = {
        'has_results': False,
        'strategy_count': 0,
        'performance_metrics': [],
        'chart_elements': [],
        'data_tables': [],
        'no_result_reasons': []
    }

    try:
        # 检查回测结果相关内容
        result_indicators = [
            ('text=回测结果', 'backtest results'),
            ('text=收益率', 'return rate'),
            ('text=年化收益', 'annualized return'),
            ('text=最大回撤', 'max drawdown'),
            ('text=夏普比率', 'sharpe ratio'),
            ('text=胜率', 'win rate'),
            ('text=净值曲线', 'nav curve'),
            ('text=收益分布', 'profit distribution'),
            ('text=总收益', 'total return'),
            ('text=交易次数', 'trade count')
        ]

        page_content = page.content().lower()

        for indicator, category in result_indicators:
            if isinstance(indicator, str) and indicator in page_content:
                results['performance_metrics'].append(f"{indicator} ({category})")
                results['has_results'] = True

        # 检查数据表格
        try:
            tables = page.locator('table').all()
            visible_tables = [table for table in tables if table.is_visible()]
            if visible_tables:
                results['data_tables'] = [f"Table {i+1}" for i in range(len(visible_tables))]
                results['has_results'] = True
                results['strategy_count'] = max(results['strategy_count'], len(visible_tables))
        except:
            pass

        # 检查图表元素
        try:
            charts = page.locator('canvas, svg, [class*="chart"], [class*="graph"]').all()
            visible_charts = [chart for chart in charts if chart.is_visible()]
            if visible_charts:
                results['chart_elements'] = [f"Chart {i+1}" for i in range(len(visible_charts))]
                results['has_results'] = True
        except:
            pass

        # 检查策略数量
        try:
            strategy_elements = page.locator('[class*="strategy"], tr, .item').all()
            visible_strategies = [el for el in strategy_elements if el.is_visible()]
            if visible_strategies:
                results['strategy_count'] = max(results['strategy_count'], len(visible_strategies))
        except:
            pass

        # 如果没有找到结果，记录原因
        if not results['has_results']:
            results['no_result_reasons'] = [
                "Backtest may still be loading",
                "Results may require login to view",
                "Page may be in intermediate state",
                "Strategy click may not have triggered backtest",
                "Data may be loading asynchronously"
            ]

    except Exception as e:
        results['no_result_reasons'].append(f"Analysis error: {e}")

    return results

def try_alternative_click_methods(page, element):
    """尝试其他点击方法"""
    print("Trying alternative click methods...")

    alternative_methods = [
        ("Double click", lambda: element.dblclick()),
        ("Right click", lambda: element.click(button='right')),
        ("Force click", lambda: element.click(force=True)),
        ("JavaScript click", lambda: page.evaluate("(el) => el.click()", element)),
        ("Hover and click", lambda: (element.hover(), time.sleep(0.5), element.click()))
    ]

    for method_name, click_method in alternative_methods:
        try:
            print(f"  Trying {method_name}...")
            click_method()
            time.sleep(2)

            # 检查是否有页面变化
            current_url = page.url
            page.wait_for_load_state('networkidle', timeout=3000)

            if page.url != current_url:
                print(f"  ✅ {method_name} successful - page changed")
                return True

        except Exception as e:
            print(f"  ❌ {method_name} failed: {e}")
            continue

    return False

if __name__ == "__main__":
    advanced_strategy_test()