from playwright.sync_api import sync_playwright
import time
import os

def test_strategy_research():
    """
    测试策略研究页面功能
    1. 访问策略研究页面
    2. 检查是否有内容（判断登录状态）
    3. 如果无内容 -> 输出登录失败
    4. 如果有内容 -> 点击策略名称进行回测
    5. 查看回测结果
    """

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        context = browser.new_context()
        page = context.new_page()

        try:
            print("=== 开始策略研究页面测试 ===")

            # 访问策略研究页面
            print("1. 正在访问策略研究页面...")

            # 尝试几个可能的策略页面URL
            strategy_urls = [
                "https://quant.10jqka.com.cn/strategy",
                "https://quant.10jqka.com.cn/strategies",
                "https://quant.10jqka.com.cn/view/strategy",
                "https://quant.10jqka.com.cn/view/strategies",
                "https://quant.10jqka.com.cn/#/strategy",
                "https://quant.10jqka.com.cn/#/strategies"
            ]

            strategy_page_loaded = False
            target_url = ""

            for url in strategy_urls:
                try:
                    print(f"  尝试访问: {url}")
                    page.goto(url, timeout=10000)
                    page.wait_for_load_state('networkidle', timeout=5000)

                    current_url = page.url
                    page_title = page.title()

                    print(f"  当前URL: {current_url}")
                    print(f"  页面标题: {page_title}")

                    # 检查是否成功加载策略页面
                    if any(keyword in page_title.lower() or keyword in current_url.lower()
                           for keyword in ['strategy', '策略', 'strategies']):
                        strategy_page_loaded = True
                        target_url = current_url
                        print(f"  ✓ 成功访问策略页面!")
                        break

                except Exception as e:
                    print(f"  ✗ 访问失败: {str(e)}")
                    continue

            if not strategy_page_loaded:
                print("\n无法访问策略页面，尝试从主页导航...")
                page.goto("https://quant.10jqka.com.cn", timeout=15000)
                page.wait_for_load_state('networkidle')

                # 查找策略研究相关的导航链接
                nav_selectors = [
                    'text=策略研究',
                    'text=策略',
                    'text=策略中心',
                    'text=回测',
                    'text=策略库',
                    '[href*="strategy"]',
                    '[href*="strategies"]'
                ]

                strategy_link_found = False
                for selector in nav_selectors:
                    try:
                        links = page.locator(selector).all()
                        for link in links:
                            if link.is_visible():
                                print(f"  找到策略链接: {selector}")
                                link.click()
                                page.wait_for_load_state('networkidle', timeout=10000)
                                strategy_link_found = True
                                break
                        if strategy_link_found:
                            break
                    except:
                        continue

                if not strategy_link_found:
                    print("  未找到策略研究页面链接")

            print(f"\n2. 检查策略页面内容...")

            # 截图保存当前状态
            screenshot_path = os.path.join(os.getcwd(), 'strategy_page.png')
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"  已保存页面截图: {screenshot_path}")

            # 检查页面内容 - 判断登录状态
            content_indicators = [
                # 策略内容相关
                ('text=策略', 'strategy content'),
                ('text=回测', 'backtest content'),
                ('text=收益', 'profit/return content'),
                ('text=夏普', 'sharpe ratio content'),

                # 登录失败相关
                ('text=登录', 'login required'),
                ('text=请登录', 'please login'),
                ('text=登录后查看', 'login to view'),
                ('text=需要登录', 'need to login'),
                ('text=登录失败', 'login failed'),
                ('text=访问受限', 'access denied'),
                ('text=权限不足', 'insufficient permissions')
            ]

            has_content = False
            login_required = False
            page_content_summary = []

            for text, category in content_indicators:
                try:
                    elements = page.locator(f'text={text}').all()
                    visible_elements = [el for el in elements if el.is_visible()]
                    if visible_elements:
                        page_content_summary.append(f"{text} ({category})")
                        if 'login' in category:
                            login_required = True
                        else:
                            has_content = True
                except:
                    continue

            print(f"  页面内容分析:")
            if page_content_summary:
                for item in page_content_summary:
                    print(f"    - {item}")
            else:
                print("    - 未发现特定内容标识")

            # 额外检查页面是否有实际的策略表格或列表
            strategy_elements = page.locator('table, .strategy, .strategy-item, .backtest, [class*="strategy"]').all()
            visible_strategy_elements = [el for el in strategy_elements if el.is_visible()]

            if visible_strategy_elements:
                has_content = True
                print(f"    - 发现 {len(visible_strategy_elements)} 个策略相关元素")

            print(f"\n3. 分析结果...")

            if not has_content and login_required:
                print("  ❌ 登录失败 - 需要登录才能访问策略研究内容")
                print("  页面显示登录提示或访问受限")

            elif has_content:
                print("  ✓ 登录成功 - 可以访问策略研究内容")
                print("  页面包含策略相关数据和功能")

                # 继续执行回测操作
                print("\n4. 查找可用的策略进行回测...")

                # 查找策略名称或回测按钮
                strategy_selectors = [
                    'text=点击回测',
                    'text=开始回测',
                    'text=回测',
                    'button:has-text("回测")',
                    '[class*="backtest"]',
                    '[class*="strategy"]',
                    'table tr',
                    '.strategy-item'
                ]

                strategy_found = False
                strategy_element = None

                for selector in strategy_selectors:
                    try:
                        elements = page.locator(selector).all()
                        visible_elements = [el for el in elements if el.is_visible()]
                        if visible_elements:
                            print(f"  找到策略元素: {selector} ({len(visible_elements)} 个)")
                            strategy_element = visible_elements[0]  # 选择第一个
                            strategy_found = True
                            break
                    except:
                        continue

                if strategy_found and strategy_element:
                    print(f"\n5. 点击策略进行回测...")

                    # 滚动到元素位置
                    strategy_element.scroll_into_view_if_needed()
                    time.sleep(1)

                    # 点击前截图
                    before_click_screenshot = os.path.join(os.getcwd(), 'strategy_before_click.png')
                    page.screenshot(path=before_click_screenshot, full_page=True)
                    print(f"  已保存点击前截图: {before_click_screenshot}")

                    # 点击策略
                    try:
                        print("  正在点击策略...")
                        strategy_element.click()

                        # 等待可能的页面变化或弹窗
                        time.sleep(3)

                        # 点击后截图
                        after_click_screenshot = os.path.join(os.getcwd(), 'strategy_after_click.png')
                        page.screenshot(path=after_click_screenshot, full_page=True)
                        print(f"  已保存点击后截图: {after_click_screenshot}")

                        # 检查回测结果
                        print("\n6. 分析回测结果...")

                        # 查找回测结果相关内容
                        result_indicators = [
                            ('text=回测结果', 'backtest results'),
                            ('text=收益率', 'return rate'),
                            ('text=最大回撤', 'max drawdown'),
                            ('text=年化收益', 'annualized return'),
                            ('text=胜率', 'win rate'),
                            ('text=夏普比率', 'sharpe ratio'),
                            ('text=净值曲线', 'nav curve'),
                            ('text=收益分布', 'profit distribution')
                        ]

                        results_found = []
                        for text, category in result_indicators:
                            try:
                                elements = page.locator(f'text={text}').all()
                                visible_elements = [el for el in elements if el.is_visible()]
                                if visible_elements:
                                    results_found.append(f"{text} ({category})")
                            except:
                                continue

                        if results_found:
                            print("  ✓ 发现回测结果:")
                            for result in results_found:
                                print(f"    - {result}")
                        else:
                            print("  - 未发现明显的回测结果")
                            print("  可能需要进一步操作或数据加载中")

                        # 检查是否有图表或数据可视化
                        charts = page.locator('canvas, svg, [class*="chart"], [class*="graph"]').all()
                        visible_charts = [chart for chart in charts if chart.is_visible()]

                        if visible_charts:
                            print(f"  ✓ 发现 {len(visible_charts)} 个图表元素")

                    except Exception as e:
                        print(f"  ✗ 点击策略时出错: {str(e)}")

                else:
                    print("  ❌ 未找到可点击的策略元素")
                    print("  页面可能需要进一步操作或权限")
            else:
                print("  ⚠️  页面状态不明确")
                print("  既没有明确的策略内容，也没有登录提示")

            # 保存最终页面HTML用于调试
            html_path = os.path.join(os.getcwd(), 'strategy_final.html')
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(page.content())
            print(f"\n7. 已保存最终页面HTML: {html_path}")

        except Exception as e:
            print(f"\n测试过程中发生错误: {str(e)}")
            import traceback
            traceback.print_exc()

        finally:
            print("\n=== 测试完成 ===")
            time.sleep(2)  # 短暂留供观察
            browser.close()

if __name__ == "__main__":
    test_strategy_research()