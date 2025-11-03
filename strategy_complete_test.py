from playwright.sync_api import sync_playwright
import time
import os

def complete_strategy_test():
    """
    完整的策略研究测试
    1. 访问主页并修复登录问题
    2. 点击策略-策略研究
    3. 检查页面内容
    4. 如果没有内容 -> 输出登录失败
    5. 如果有内容 -> 点击策略名称进行回测
    6. 查看回测结果
    """

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=800)
        context = browser.new_context()
        page = context.new_page()

        try:
            print("=== Complete Strategy Research Test ===")

            # 第一步：访问主页并修复登录问题
            print("1. Accessing main page...")
            page.goto("https://quant.10jqka.com.cn", timeout=30000)
            page.wait_for_load_state('networkidle')
            print(f"Main page loaded: {page.title()}")

            # 应用登录修复 - 移除遮罩层并强制显示登录弹窗
            print("2. Applying login fix...")

            # 检查并移除遮罩层
            mask_exists = page.evaluate("""
                () => {
                    const masks = document.querySelectorAll('[id*="mask"], [id*="overlay"]');
                    const loginMask = document.getElementById('ths_iframe_login_mask');

                    let masksRemoved = 0;
                    masks.forEach(mask => {
                        if (mask.id && mask.id.includes('mask')) {
                            mask.remove();
                            masksRemoved++;
                        }
                    });

                    if (loginMask) {
                        loginMask.remove();
                        masksRemoved++;
                    }

                    return {
                        masksRemoved: masksRemoved,
                        loginMaskRemoved: loginMask ? true : false
                    };
                }
            """)

            print(f"  - Masks removed: {mask_exists['masksRemoved']}")
            print(f"  - Login mask removed: {mask_exists['loginMaskRemoved']}")

            # 强制显示隐藏的登录对话框
            page.evaluate("""
                () => {
                    const dialogs = document.querySelectorAll('[class*="dialog"], [class*="modal"], [class*="overlay"]');
                    dialogs.forEach(dialog => {
                        const style = getComputedStyle(dialog);
                        if (style.display === 'block' && style.visibility === 'visible') {
                            dialog.style.display = 'block';
                            dialog.style.visibility = 'visible';
                            dialog.style.zIndex = '9999';
                            dialog.style.position = 'fixed';
                            dialog.style.top = '50%';
                            dialog.style.left = '50%';
                            dialog.style.transform = 'translate(-50%, -50%)';
                            dialog.style.backgroundColor = 'white';
                            dialog.style.border = '1px solid #ccc';
                            dialog.style.borderRadius = '8px';
                            dialog.style.padding = '20px';
                            dialog.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
                        }
                    });
                    return dialogs.length;
                }
            """)

            time.sleep(2)

            # 尝试登录（如果需要）
            print("3. Checking if login is needed...")
            login_button = page.locator('a.login').first
            if login_button.is_visible():
                print("  - Login button is visible, attempting to show login form...")
                try:
                    login_button.click()
                    time.sleep(3)
                    print("  - Login form should now be visible")
                except Exception as e:
                    print(f"  - Login click failed: {e}")

            # 第二步：点击策略研究
            print("4. Looking for strategy research navigation...")
            time.sleep(2)

            strategy_selectors = [
                'text=策略研究',
                'a:has-text("策略研究")',
                '[href*="study-index"]'
            ]

            strategy_link = None
            for selector in strategy_selectors:
                try:
                    elements = page.locator(selector).all()
                    for element in elements:
                        if element.is_visible():
                            strategy_link = element
                            print(f"  - Found strategy research link: {selector}")
                            break
                except:
                    continue

            if not strategy_link:
                print("  - Strategy research link not found")
                print("  - Checking current page for content...")

                # 分析当前页面内容
                content_status = analyze_current_content(page)

                if not content_status['has_content'] and content_status['requires_login']:
                    print("\n❌ LOGIN FAILED - No strategy content available")
                    print("Reasons:")
                    for reason in content_status['login_indicators']:
                        print(f"    - {reason}")
                else:
                    print("\n✅ CONTENT FOUND - Strategy content is available")
                    for feature in content_status['content_features']:
                        print(f"    - {feature}")

                    # 查找策略项目进行回测
                    if content_status['strategy_items']:
                        print("\n5. Looking for strategy items to backtest...")
                        try_backtest_on_page(page)
                    else:
                        print("\n❌ NO STRATEGY ITEMS FOUND")

            else:
                print("5. Clicking on strategy research link...")

                # 截图保存点击前状态
                before_click_screenshot = os.path.join(os.getcwd(), 'strategy_before_final_click.png')
                page.screenshot(path=before_click_screenshot, full_page=True)
                print(f"  - Screenshot before click: {before_click_screenshot}")

                try:
                    # 滚动到元素位置
                    strategy_link.scroll_into_view_if_needed()
                    time.sleep(1)

                    # 点击策略研究链接
                    print("  - Clicking strategy research link...")
                    strategy_link.click()
                    page.wait_for_load_state('networkidle', timeout=15000)

                    # 点击后截图
                    after_click_screenshot = os.path.join(os.getcwd(), 'strategy_after_final_click.png')
                    page.screenshot(path=after_click_screenshot, full_page=True)
                    print(f"  - Screenshot after click: {after_click_screenshot}")

                    print(f"  - Current URL: {page.url()}")
                    print(f"  - Page title: {page.title()}")

                    # 分析策略研究页面内容
                    print("6. Analyzing strategy research page content...")
                    content_analysis = analyze_strategy_page_content(page)

                    if not content_analysis['has_strategy_content'] and content_analysis['requires_login']:
                        print("\n❌ LOGIN FAILED - Strategy research page requires login")
                        print("Reasons:")
                        for reason in content_analysis['login_indicators']:
                            print(f"    - {reason}")

                    elif content_analysis['has_strategy_content']:
                        print("\n✅ STRATEGY CONTENT FOUND - Strategy research content is available")
                        print("Available features:")
                        for feature in content_analysis['strategy_features']:
                            print(f"    - {feature}")

                        # 查找策略项目进行回测
                        if content_analysis['strategy_items']:
                            print("\n7. Looking for strategy items to backtest...")
                            try_backtest_on_page(page)
                        else:
                            print("\n❌ NO STRATEGY ITEMS FOUND TO BACKTEST")

                    else:
                        print("\n⚠️ UNCLEAR CONTENT STATUS")

                except Exception as e:
                    print(f"  - Error clicking strategy link: {e}")

            # 保存最终状态
            final_screenshot = os.path.join(os.getcwd(), 'strategy_complete_final.png')
            page.screenshot(path=final_screenshot, full_page=True)
            print(f"\n8. Final screenshot: {final_screenshot}")

            # 保存HTML
            html_path = os.path.join(os.getcwd(), 'strategy_complete_final.html')
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(page.content())
            print(f"   Final HTML: {html_path}")

        except Exception as e:
            print(f"\nTest error: {e}")
            import traceback
            traceback.print_exc()

        finally:
            time.sleep(2)
            browser.close()
            print("\n=== Test Completed ===")

def analyze_current_content(page):
    """分析当前页面内容"""
    analysis = {
        'has_content': False,
        'requires_login': False,
        'login_indicators': [],
        'content_features': [],
        'strategy_items': []
    }

    page_content = page.content().lower()

    # 检查登录相关元素
    login_indicators = ['登录', 'login', '请登录', '需要登录']
    for indicator in login_indicators:
        if indicator in page_content:
            analysis['login_indicators'].append(f"Found login indicator: {indicator}")
            analysis['requires_login'] = True

    # 检查策略内容特征
    strategy_features = ['策略', 'strategy', '回测', 'backtest', '收益', '策略库']
    for feature in strategy_features:
        if feature in page_content:
            analysis['content_features'].append(f"Found feature: {feature}")
            analysis['has_content'] = True

    # 检查策略项目
    strategy_item_selectors = ['tr', 'table', '.strategy', '.item', '.backtest']
    for selector in strategy_item_selectors:
        try:
            elements = page.locator(selector).all()
            visible_elements = [el for el in elements if el.is_visible()]
            if visible_elements:
                analysis['strategy_items'].append(f"Found items with {selector}: {len(visible_elements)}")
                analysis['has_content'] = True
        except:
            continue

    return analysis

def analyze_strategy_page_content(page):
    """分析策略研究页面内容"""
    analysis = {
        'has_strategy_content': False,
        'requires_login': False,
        'login_indicators': [],
        'strategy_features': [],
        'strategy_items': []
    }

    page_content = page.content().lower()

    # 检查登录要求
    login_indicators = ['请登录', '需要登录', '登录后查看', '权限不足', '访问受限']
    for indicator in login_indicators:
        if indicator in page_content:
            analysis['login_indicators'].append(f"Found login requirement: {indicator}")
            analysis['requires_login'] = True

    # 检查策略功能
    strategy_features = [
        ('策略创建', 'strategy creation'),
        ('策略编辑', 'strategy editing'),
        ('策略列表', 'strategy list'),
        ('回测功能', 'backtest'),
        ('策略分析', 'strategy analysis'),
        ('我的策略', 'my strategies'),
        ('策略库', 'strategy library')
    ]

    for feature, category in strategy_features:
        if feature in page_content:
            analysis['strategy_features'].append(f"Found {feature} ({category})")
            analysis['has_strategy_content'] = True

    # 检查策略项目
    strategy_selectors = [
        ('table tr', 'strategy tables'),
        ('.strategy-item', 'strategy items'),
        ('.backtest-item', 'backtest items'),
        ('[class*="strategy"]', 'strategy elements'),
        ('button:has-text("回测")', 'backtest buttons'),
        ('a:has-text("详情")', 'strategy detail links')
    ]

    for selector in strategy_selectors:
        try:
            elements = page.locator(selector).all()
            visible_elements = [el for el in elements if el.is_visible()]
            if visible_elements:
                analysis['strategy_items'].append(f"Found strategy items with {selector}: {len(visible_elements)}")
                analysis['has_strategy_content'] = True
        except:
            continue

    return analysis

def try_backtest_on_page(page):
    """在页面上尝试回测操作"""
    print("8. Attempting backtest operations...")

    # 查找可点击的策略项目
    strategy_selectors = [
        'table tr:has-text)',
        '.strategy-item',
        '.backtest-item',
        '[class*="strategy"]:visible',
        'button:has-text("回测"):visible',
        'a:has-text("详情"):visible'
    ]

    strategy_found = False
    strategy_element = None

    for selector in strategy_selectors:
        try:
            elements = page.locator(selector).all()
            visible_elements = [el for el in elements if el.is_visible()]
            if visible_elements:
                strategy_element = visible_elements[0]
                strategy_found = True
                print(f"  - Found strategy item: {selector}")
                break
        except:
            continue

    if strategy_found and strategy_element:
        try:
            # 获取策略名称
            strategy_name = get_strategy_name(strategy_element)
            print(f"  - Selected strategy: {strategy_name}")

            # 滚动到策略位置
            strategy_element.scroll_into_view_if_needed()
            time.sleep(1)

            # 截图保存点击前状态
            before_backtest_screenshot = os.path.join(os.getcwd(), 'backtest_before.png')
            page.screenshot(path=before_backtest_screenshot, full_page=True)
            print(f"  - Screenshot before backtest: {before_backtest_screenshot}")

            # 尝试多种点击方法
            click_methods = [
                ("Normal click", lambda: strategy_element.click()),
                ("Double click", lambda: strategy_element.dblclick()),
                ("Right click", lambda: strategy_element.click(button='right')),
                ("JavaScript click", lambda: page.evaluate("(el) => el.click()", strategy_element))
            ]

            for method_name, click_method in click_methods:
                try:
                    print(f"  - Trying {method_name}...")
                    click_method()
                    time.sleep(3)

                    # 检查页面变化
                    page.wait_for_load_state('networkidle', timeout=5000)

                    # 分析回测结果
                    backtest_results = analyze_backtest_results(page)

                    if backtest_results['has_results']:
                        print(f"  - ✅ {method_name} successful! Backtest results found:")
                        print(f"    - Charts: {backtest_results['chart_count']}")
                        print(f"    - Performance metrics: {len(backtest_results['performance_metrics'])}")
                        print(f"    - Data tables: {backtest_results['table_count']}")

                        # 截图保存回测结果
                        after_backtest_screenshot = os.path.join(os.getcwd(), 'backtest_success.png')
                        page.screenshot(path=after_backtest_screenshot, full_page=True)
                        print(f"  - Backtest success screenshot: {after_backtest_screenshot}")
                        return True

                except Exception as e:
                    print(f"  - {method_name} failed: {e}")
                    continue

            print("  - All click methods attempted")
            print("  - ❌ NO BACKTEST RESULTS FOUND")

        except Exception as e:
            print(f"  - Error during backtest attempt: {e}")

    return False

def get_strategy_name(element):
    """获取策略名称"""
    try:
        # 尝试多种方式获取名称
        name_methods = [
            lambda: element.inner_text().strip(),
            lambda: element.get_attribute('title') or "",
            lambda: element.get_attribute('data-name') or "",
            lambda: element.locator('td:first-child').inner_text().strip() if element.locator('td:first-child').count() > 0 else "",
            lambda: element.locator('.name').inner_text().strip() if element.locator('.name').count() > 0 else ""
        ]

        for method in name_methods:
            try:
                name = method()
                if name and len(name) > 0 and len(name) < 100:
                    return name[:50]  # 限制长度
            except:
                continue
    except:
        pass

    return "Unknown Strategy"

def analyze_backtest_results(page):
    """分析回测结果"""
    results = {
        'has_results': False,
        'chart_count': 0,
        'table_count': 0,
        'performance_metrics': []
    }

    page_content = page.content().lower()

    # 检查回测相关内容
    result_indicators = [
        ('回测结果', 'backtest results'),
        ('收益率', 'return rate'),
        ('年化收益', 'annualized return'),
        ('最大回撤', 'max drawdown'),
        ('夏普比率', 'sharpe ratio'),
        ('胜率', 'win rate'),
        ('净值曲线', 'nav curve'),
        ('收益分布', 'profit distribution'),
        ('总收益', 'total return'),
        ('交易次数', 'trade count')
    ]

    for indicator, category in result_indicators:
        if indicator in page_content:
            results['performance_metrics'].append(f"{indicator} ({category})")
            results['has_results'] = True

    # 检查图表元素
    try:
        charts = page.locator('canvas, svg, [class*="chart"], [class*="graph"]').all()
        visible_charts = [chart for chart in charts if chart.is_visible()]
        results['chart_count'] = len(visible_charts)
        if visible_charts:
            results['has_results'] = True
    except:
        pass

    # 检查数据表格
    try:
        tables = page.locator('table').all()
        visible_tables = [table for table in tables if table.is_visible()]
        results['table_count'] = len(visible_tables)
        if visible_tables:
            results['has_results'] = True
    except:
        pass

    return results

if __name__ == "__main__":
    complete_strategy_test()