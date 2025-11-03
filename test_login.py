from playwright.sync_api import sync_playwright
import time

def test_quant_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 设置为非无头模式以便观察
        page = browser.new_page()

        try:
            print("正在访问 https://quant.10jqka.com.cn...")
            page.goto('https://quant.10jqka.com.cn')

            # 等待页面加载完成
            page.wait_for_load_state('networkidle')

            # 截图保存页面状态
            page.screenshot(path='/tmp/quant_homepage.png', full_page=True)
            print("已保存首页截图到 /tmp/quant_homepage.png")

            # 尝试查找登录按钮
            print("正在查找登录按钮...")

            # 常见的登录按钮选择器
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
                'div:has-text("登录")',
                '.login-btn',
                '.signin-btn'
            ]

            login_element = None
            for selector in login_selectors:
                try:
                    element = page.locator(selector).first
                    if element.is_visible():
                        login_element = element
                        print(f"找到登录按钮: {selector}")
                        break
                except:
                    continue

            if not login_element:
                # 打印页面内容帮助调试
                print("未找到登录按钮，打印页面内容...")
                content = page.content()
                print(f"页面标题: {page.title()}")
                print("页面中的所有按钮和链接:")
                buttons = page.locator('button, a').all()
                for i, btn in enumerate(buttons[:10]):  # 只显示前10个
                    try:
                        text = btn.inner_text()
                        print(f"  {i+1}. 文本: '{text}', 选择器: {btn}")
                    except:
                        print(f"  {i+1}. 无法获取文本")

                # 保存页面HTML到文件
                with open('/tmp/quant_page.html', 'w', encoding='utf-8') as f:
                    f.write(content)
                print("已保存页面HTML到 /tmp/quant_page.html")
            else:
                print("点击登录按钮...")
                login_element.click()

                # 等待可能的响应或错误
                time.sleep(3)

                # 检查控制台错误
                console_messages = []
                page.on('console', lambda msg: console_messages.append(f"{msg.type}: {msg.text}"))

                # 截图保存点击后的状态
                page.screenshot(path='/tmp/quant_after_login_click.png', full_page=True)
                print("已保存点击登录按钮后的截图到 /tmp/quant_after_login_click.png")

                # 检查是否有错误消息
                error_selectors = [
                    '.error-message',
                    '.alert-error',
                    '[class*="error"]',
                    'text=错误',
                    'text=失败',
                    'text=抱歉'
                ]

                for error_selector in error_selectors:
                    try:
                        error_element = page.locator(error_selector).first
                        if error_element.is_visible():
                            error_text = error_element.inner_text()
                            print(f"发现错误信息: {error_text}")
                    except:
                        continue

                if console_messages:
                    print("控制台消息:")
                    for msg in console_messages:
                        print(f"  {msg}")

        except Exception as e:
            print(f"发生错误: {str(e)}")
            # 即使出错也保存截图
            try:
                page.screenshot(path='/tmp/quant_error.png', full_page=True)
                print("已保存错误状态的截图到 /tmp/quant_error.png")
            except:
                pass
        finally:
            browser.close()

if __name__ == "__main__":
    test_quant_login()