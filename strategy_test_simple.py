from playwright.sync_api import sync_playwright
import time
import os

def simple_strategy_test():
    """简化的策略测试，避免编码问题"""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        context = browser.new_context()
        page = context.new_page()

        try:
            print("Starting strategy research test...")

            # 先访问主页
            print("1. Accessing main page...")
            page.goto("https://quant.10jqka.com.cn", timeout=30000)
            page.wait_for_load_state('networkidle')
            print(f"Main page loaded: {page.title()}")

            # 查找策略相关的导航
            print("2. Looking for strategy navigation...")

            navigation_links = []
            try:
                # 查找页面中的所有链接
                links = page.locator('a').all()
                for link in links[:50]:  # 只检查前50个链接
                    try:
                        text = link.inner_text().strip()
                        href = link.get_attribute('href')
                        if href and any(keyword in text.lower() for keyword in ['strategy', '策略', 'strategies']):
                            navigation_links.append({'text': text, 'href': href})
                            print(f"Found link: {text} -> {href}")
                    except:
                        continue
            except Exception as e:
                print(f"Error finding links: {e}")

            if not navigation_links:
                print("No strategy navigation found, checking page content...")
                # 检查页面是否有登录要求
                page_content = page.content()

                # 检查登录相关文本
                login_indicators = ['login', 'login', 'sign in', '登录', '请登录', '需要登录']
                has_login_requirement = any(indicator in page_content.lower() for indicator in login_indicators)

                if has_login_requirement:
                    print("LOGIN FAILED - Page requires login to access strategy content")
                else:
                    print("Page content check completed")

            else:
                print(f"Found {len(navigation_links)} strategy-related links")

                # 尝试点击第一个策略链接
                if navigation_links:
                    first_link = navigation_links[0]
                    print(f"3. Clicking on: {first_link['text']}")

                    try:
                        # 查找并点击链接
                        link_element = page.locator(f'text={first_link["text"]}').first
                        if link_element.is_visible():
                            link_element.click()
                            page.wait_for_load_state('networkidle', timeout=10000)

                            print(f"Navigated to: {page.url()}")
                            print(f"Page title: {page.title()}")

                            # 截图
                            screenshot_path = os.path.join(os.getcwd(), 'strategy_page.png')
                            page.screenshot(path=screenshot_path, full_page=True)
                            print(f"Screenshot saved: {screenshot_path}")

                            # 检查是否有策略内容
                            print("4. Checking for strategy content...")

                            # 查找策略相关元素
                            strategy_elements = page.locator('table, .strategy, .backtest, .result, .chart, canvas').all()
                            visible_elements = [el for el in strategy_elements if el.is_visible()]

                            if visible_elements:
                                print(f"SUCCESS - Found {len(visible_elements)} strategy elements")

                                # 尝试点击第一个策略项目
                                print("5. Looking for clickable strategy items...")

                                clickable_items = page.locator('tr, button, .strategy-item, [onclick]').all()
                                visible_clickables = [item for item in clickable_items if item.is_visible()]

                                if visible_clickables:
                                    first_item = visible_clickables[0]
                                    print("Clicking on first strategy item...")

                                    # 点击前截图
                                    before_screenshot = os.path.join(os.getcwd(), 'strategy_before_click.png')
                                    page.screenshot(path=before_screenshot, full_page=True)

                                    first_item.click()
                                    time.sleep(3)

                                    # 点击后截图
                                    after_screenshot = os.path.join(os.getcwd(), 'strategy_after_click.png')
                                    page.screenshot(path=after_screenshot, full_page=True)

                                    print("Checking for backtest results...")

                                    # 查找回测结果
                                    result_keywords = ['result', 'backtest', 'return', 'profit', '收益', '回测', '结果']
                                    page_content_after = page.content()
                                    has_results = any(keyword in page_content_after.lower() for keyword in result_keywords)

                                    if has_results:
                                        print("SUCCESS - Backtest results found!")
                                    else:
                                        print("No backtest results visible")
                                else:
                                    print("No clickable strategy items found")
                            else:
                                print("No strategy content found - may need login")

                                # 检查是否有登录提示
                                login_keywords = ['login', 'sign in', '登录', '请登录']
                                has_login_prompt = any(keyword in page_content_after.lower() for keyword in login_keywords)

                                if has_login_prompt:
                                    print("LOGIN REQUIRED - Page shows login prompts")

                    except Exception as click_error:
                        print(f"Error clicking link: {click_error}")

            print("6. Saving final page state...")
            final_screenshot = os.path.join(os.getcwd(), 'strategy_final.png')
            page.screenshot(path=final_screenshot, full_page=True)

            # 保存HTML
            html_path = os.path.join(os.getcwd(), 'strategy_final.html')
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(page.content())
            print(f"Final HTML saved: {html_path}")

        except Exception as e:
            print(f"Test error: {e}")
            import traceback
            traceback.print_exc()

            # 错误截图
            try:
                error_screenshot = os.path.join(os.getcwd(), 'strategy_error.png')
                page.screenshot(path=error_screenshot, full_page=True)
                print(f"Error screenshot saved: {error_screenshot}")
            except:
                pass

        finally:
            time.sleep(2)
            browser.close()
            print("Test completed")

if __name__ == "__main__":
    simple_strategy_test()