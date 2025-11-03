from playwright.sync_api import sync_playwright
import time
import os

def detailed_login_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)  # 非无头模式，慢动作便于观察
        page = browser.new_page()

        try:
            print("正在访问 https://quant.10jqka.com.cn...")
            page.goto('https://quant.10jqka.com.cn', timeout=30000)

            # 等待页面加载完成
            page.wait_for_load_state('networkidle')

            print("页面标题:", page.title())

            # 尝试查找登录按钮
            print("正在查找登录按钮...")
            login_selectors = [
                'text=登录',
                'text=登陆',
                'text=登录/注册',
                'text=请登录',
                '[class*="login"]',
                '[class*="signin"]',
                '[id*="login"]',
                '[id*="signin"]',
                'a[href*="login"]',
                'button:has-text("登录")',
                'div:has-text("登录")'
            ]

            login_element = None
            for selector in login_selectors:
                try:
                    elements = page.locator(selector).all()
                    if elements:
                        for i, element in enumerate(elements):
                            if element.is_visible():
                                login_element = element
                                print(f"找到可见的登录按钮: {selector} (第{i+1}个)")
                                break
                        if login_element:
                            break
                except Exception as e:
                    continue

            if not login_element:
                print("未找到可见的登录按钮，显示页面内容...")
                # 保存页面HTML
                html_path = os.path.join(os.getcwd(), 'quant_page.html')
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(page.content())
                print(f"已保存页面HTML到 {html_path}")

                # 显示页面中的所有文本元素
                print("页面中的主要文本元素:")
                text_elements = page.locator('text=*').all()
                for i, element in enumerate(text_elements[:20]):  # 只显示前20个
                    try:
                        text = element.inner_text().strip()
                        if len(text) > 0 and len(text) < 100:  # 过滤掉过长的文本
                            print(f"  {i+1}. '{text}'")
                    except:
                        continue
            else:
                print("登录按钮信息:")
                try:
                    print(f"  - 文本: '{login_element.inner_text()}'")
                    print(f"  - 标签: {login_element.evaluate('el => el.tagName')}")
                    print(f"  - 类型: {login_element.evaluate('el => el.type')}")
                    print(f"  - 类名: {login_element.evaluate('el => el.className')}")
                    print(f"  - ID: {login_element.evaluate('el => el.id')}")
                    print(f"  - href: {login_element.evaluate('el => el.href')}")
                except Exception as e:
                    print(f"获取元素信息时出错: {e}")

                # 滚动到登录按钮位置
                login_element.scroll_into_view_if_needed()
                time.sleep(1)

                # 点击前截图
                screenshot_before = os.path.join(os.getcwd(), 'quant_before_click.png')
                page.screenshot(path=screenshot_before, full_page=True)
                print(f"已保存点击前截图到 {screenshot_before}")

                print("正在点击登录按钮...")
                login_element.click()

                # 等待可能的响应
                time.sleep(5)

                # 点击后截图
                screenshot_after = os.path.join(os.getcwd(), 'quant_after_click.png')
                page.screenshot(path=screenshot_after, full_page=True)
                print(f"已保存点击后截图到 {screenshot_after}")

                # 检查页面URL变化
                current_url = page.url
                print(f"点击后页面URL: {current_url}")

                # 检查是否有弹出窗口或新页面
                try:
                    # 检查控制台错误
                    console_errors = []
                    page.on('console', lambda msg: console_errors.append(f"{msg.type}: {msg.text}") if msg.type == 'error' else None)

                    # 检查页面错误
                    page_errors = []
                    page.on('pageerror', lambda error: page_errors.append(str(error)))

                    # 重新加载页面触发错误收集
                    time.sleep(2)

                    if console_errors:
                        print("控制台错误:")
                        for error in console_errors:
                            print(f"  {error}")

                    if page_errors:
                        print("页面错误:")
                        for error in page_errors:
                            print(f"  {error}")
                except Exception as e:
                    print(f"收集错误信息时出错: {e}")

                # 检查是否有登录表单出现
                login_form_selectors = [
                    'input[type="text"]',
                    'input[type="password"]',
                    'input[name*="username"]',
                    'input[name*="password"]',
                    'input[placeholder*="用户"]',
                    'input[placeholder*="账号"]',
                    'input[placeholder*="手机"]',
                    'input[placeholder*="密码"]'
                ]

                found_form = False
                for form_selector in login_form_selectors:
                    try:
                        elements = page.locator(form_selector).all()
                        visible_elements = [el for el in elements if el.is_visible()]
                        if visible_elements:
                            found_form = True
                            print(f"发现登录表单元素: {form_selector}")
                            for i, element in enumerate(visible_elements):
                                try:
                                    placeholder = element.evaluate('el => el.placeholder')
                                    name = element.evaluate('el => el.name')
                                    print(f"  元素{i+1}: name='{name}', placeholder='{placeholder}'")
                                except:
                                    print(f"  元素{i+1}: 无法获取详细信息")
                    except:
                        continue

                if not found_form:
                    print("未发现登录表单元素")
                    print("当前页面标题:", page.title())

                    # 检查是否有错误消息
                    error_texts = ['错误', '失败', '抱歉', '无法访问', '请重试', '登录失败']
                    for error_text in error_texts:
                        try:
                            error_elements = page.locator(f'text={error_text}').all()
                            visible_errors = [el for el in error_elements if el.is_visible()]
                            if visible_errors:
                                for error_el in visible_errors:
                                    error_message = error_el.inner_text()
                                    print(f"发现错误消息: {error_message}")
                        except:
                            continue

        except Exception as e:
            print(f"发生错误: {str(e)}")
            import traceback
            traceback.print_exc()

            # 错误状态下截图
            try:
                error_screenshot = os.path.join(os.getcwd(), 'quant_error.png')
                page.screenshot(path=error_screenshot, full_page=True)
                print(f"已保存错误状态截图到 {error_screenshot}")
            except:
                pass
        finally:
            browser.close()

if __name__ == "__main__":
    detailed_login_test()