from playwright.sync_api import sync_playwright
import time
import os

def analyze_login_issue():
    with sync_playwright() as p:
        # 启用开发者工具，禁用弹窗阻止
        browser = p.chromium.launch(
            headless=False,
            slow_mo=500,
            args=[
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor',
                '--no-sandbox',
                '--disable-setuid-sandbox'
            ]
        )

        context = browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )

        page = context.new_page()

        try:
            print("正在访问 https://quant.10jqka.com.cn...")
            page.goto('https://quant.10jqka.com.cn', timeout=30000)

            # 等待页面加载完成
            page.wait_for_load_state('networkidle')
            print("页面标题:", page.title())

            # 检查页面中的JavaScript
            print("\n=== 检查JavaScript对象 ===")

            # 检查LoginInstance是否存在
            login_instance_exists = page.evaluate("() => typeof window.LoginInstance !== 'undefined'")
            print(f"LoginInstance对象存在: {login_instance_exists}")

            if login_instance_exists:
                show_method_exists = page.evaluate("() => typeof window.LoginInstance.show === 'function'")
                print(f"show方法存在: {show_method_exists}")

                if show_method_exists:
                    # 尝试直接调用show方法
                    print("尝试直接调用 window.LoginInstance.show()...")
                    try:
                        result = page.evaluate("() => { try { window.LoginInstance.show(); return 'success'; } catch(e) { return e.toString(); } }")
                        print(f"调用结果: {result}")
                    except Exception as e:
                        print(f"JavaScript执行错误: {e}")
                else:
                    print("LoginInstance.show方法不存在")
            else:
                print("LoginInstance对象不存在")

                # 检查页面中是否有其他登录相关的JavaScript
                print("\n=== 搜索登录相关的JavaScript对象 ===")
                js_objects = page.evaluate("""
                    () => {
                        const loginRelated = [];
                        for (let key in window) {
                            if (key.toLowerCase().includes('login') ||
                                key.toLowerCase().includes('auth') ||
                                key.toLowerCase().includes('sign')) {
                                loginRelated.push({
                                    name: key,
                                    type: typeof window[key],
                                    hasShow: typeof window[key] === 'object' && typeof window[key].show === 'function'
                                });
                            }
                        }
                        return loginRelated;
                    }
                """)

                if js_objects:
                    print("发现登录相关的JavaScript对象:")
                    for obj in js_objects:
                        print(f"  - {obj['name']} ({obj['type']})" + (", 有show方法" if obj['hasShow'] else ""))
                else:
                    print("未发现登录相关的JavaScript对象")

            # 检查是否有隐藏的登录弹窗
            print("\n=== 检查隐藏的登录弹窗 ===")

            login_dialog_selectors = [
                '.login-dialog',
                '.login-modal',
                '.login-popup',
                '.login-form',
                '[class*="modal"]',
                '[class*="dialog"]',
                '[class*="popup"]',
                '#login',
                '#loginDialog',
                '#loginModal'
            ]

            for selector in login_dialog_selectors:
                try:
                    elements = page.locator(selector).all()
                    if elements:
                        print(f"发现可能的登录对话框: {selector}")
                        for i, element in enumerate(elements):
                            is_visible = element.is_visible()
                            display_style = element.evaluate('el => getComputedStyle(el).display')
                            visibility_style = element.evaluate('el => getComputedStyle(el).visibility')
                            print(f"  元素{i+1}: 可见={is_visible}, display={display_style}, visibility={visibility_style}")
                except:
                    continue

            # 尝试点击登录按钮并观察变化
            print("\n=== 点击登录按钮观察变化 ===")

            login_button = page.locator('a.login').first
            if login_button.is_visible():
                print("点击登录按钮...")

                # 记录点击前的DOM状态
                before_click = page.evaluate("""
                    () => {
                        const dialogs = document.querySelectorAll('.modal, .dialog, .popup, [class*="login"]');
                        return Array.from(dialogs).map(el => ({
                            className: el.className,
                            display: getComputedStyle(el).display,
                            visibility: getComputedStyle(el).visibility,
                            innerHTML: el.innerHTML.substring(0, 100)
                        }));
                    }
                """)

                login_button.click()

                # 等待可能的DOM变化
                time.sleep(3)

                # 记录点击后的DOM状态
                after_click = page.evaluate("""
                    () => {
                        const dialogs = document.querySelectorAll('.modal, .dialog, .popup, [class*="login"]');
                        return Array.from(dialogs).map(el => ({
                            className: el.className,
                            display: getComputedStyle(el).display,
                            visibility: getComputedStyle(el).visibility,
                            innerHTML: el.innerHTML.substring(0, 100)
                        }));
                    }
                """)

                print("点击前DOM状态:", len(before_click))
                print("点击后DOM状态:", len(after_click))

                if len(after_click) > len(before_click):
                    print("发现新增的DOM元素，可能是登录弹窗")
                    for i, element in enumerate(after_click):
                        if element not in before_click:
                            print(f"  新元素{i+1}: {element['className']}")

                # 检查URL变化
                print(f"当前URL: {page.url}")

                # 截图保存当前状态
                screenshot_path = os.path.join(os.getcwd(), 'login_analysis.png')
                page.screenshot(path=screenshot_path, full_page=True)
                print(f"已保存截图到: {screenshot_path}")

        except Exception as e:
            print(f"分析过程中发生错误: {str(e)}")
            import traceback
            traceback.print_exc()

            # 错误状态截图
            try:
                error_screenshot = os.path.join(os.getcwd(), 'analysis_error.png')
                page.screenshot(path=error_screenshot, full_page=True)
                print(f"已保存错误状态截图到: {error_screenshot}")
            except:
                pass

        finally:
            browser.close()

if __name__ == "__main__":
    analyze_login_issue()