from playwright.sync_api import sync_playwright
import time
import os

def login_fix():
    """
    修复登录功能的解决方案

    问题根源：
    1. 登录按钮被一个遮罩层 <div id="ths_iframe_login_mask"></div> 拦截点击事件
    2. LoginInstance.show() 方法可以正常工作，但按钮点击被阻止

    解决方案：
    1. 移除或隐藏遮罩层
    2. 直接调用JavaScript触发登录弹窗
    3. 强制点击登录按钮
    """

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        context = browser.new_context()
        page = context.new_page()

        try:
            print("正在访问 https://quant.10jqka.com.cn...")
            page.goto('https://quant.10jqka.com.cn', timeout=30000)
            page.wait_for_load_state('networkidle')

            print("=== 解决方案1: 移除遮罩层后点击 ===")

            # 检查遮罩层是否存在
            mask_exists = page.evaluate("() => document.getElementById('ths_iframe_login_mask') !== null")
            print(f"登录遮罩层存在: {mask_exists}")

            if mask_exists:
                # 移除遮罩层
                page.evaluate("() => { const mask = document.getElementById('ths_iframe_login_mask'); if (mask) mask.remove(); }")
                print("已移除登录遮罩层")

                # 等待一下让页面稳定
                time.sleep(1)

                # 点击登录按钮
                login_button = page.locator('a.login').first
                if login_button.is_visible():
                    print("点击登录按钮...")
                    login_button.click()

                    # 等待登录弹窗出现
                    time.sleep(3)

                    # 检查登录表单是否出现
                    login_forms = page.locator('input[type="text"], input[type="password"]').all()
                    visible_forms = [form for form in login_forms if form.is_visible()]

                    if visible_forms:
                        print(f"✅ 成功！发现 {len(visible_forms)} 个可见的登录表单元素")
                        for i, form in enumerate(visible_forms):
                            placeholder = form.evaluate('el => el.placeholder || ""')
                            print(f"  表单{i+1}: placeholder='{placeholder}'")
                    else:
                        print("❌ 仍未显示登录表单")
                else:
                    print("❌ 登录按钮不可见")
            else:
                print("未发现遮罩层，尝试其他方法")

            print("\n=== 解决方案2: 直接调用JavaScript ===")

            # 尝试不同的JavaScript方法触发登录
            js_methods = [
                "window.LoginInstance.show()",
                "if (window.LoginInstance && window.LoginInstance.show) window.LoginInstance.show()",
                "$(document).ready(function() { if (window.LoginInstance) window.LoginInstance.show(); })"
            ]

            for i, js_method in enumerate(js_methods):
                print(f"尝试方法 {i+1}: {js_method[:50]}...")
                try:
                    result = page.evaluate(f"() => {{ {js_method}; return 'success'; }}")
                    print(f"  结果: {result}")

                    # 等待可能的响应
                    time.sleep(2)

                    # 检查登录表单
                    login_forms = page.locator('input[type="text"], input[type="password"]').all()
                    visible_forms = [form for form in login_forms if form.is_visible()]

                    if visible_forms:
                        print(f"✅ 方法 {i+1} 成功！发现 {len(visible_forms)} 个登录表单")
                        break
                except Exception as e:
                    print(f"  失败: {str(e)}")

            print("\n=== 解决方案3: 强制显示隐藏的登录对话框 ===")

            # 显示隐藏的对话框
            hidden_dialogs = page.evaluate("""
                () => {
                    const dialogs = document.querySelectorAll('[class*="dialog"]');
                    const results = [];
                    dialogs.forEach((dialog, index) => {
                        const style = getComputedStyle(dialog);
                        if (style.display === 'block' && style.visibility === 'visible' && !dialog.offsetParent) {
                            dialog.style.display = 'block';
                            dialog.style.visibility = 'visible';
                            dialog.style.zIndex = '9999';
                            dialog.style.position = 'fixed';
                            dialog.style.top = '50%';
                            dialog.style.left = '50%';
                            dialog.style.transform = 'translate(-50%, -50%)';
                            results.push({
                                index: index,
                                className: dialog.className,
                                innerHTML: dialog.innerHTML.substring(0, 200)
                            });
                        }
                    });
                    return results;
                }
            """)

            if hidden_dialogs:
                print(f"已显示 {len(hidden_dialogs)} 个隐藏的对话框")
                for dialog in hidden_dialogs:
                    print(f"  对话框 {dialog['index']}: {dialog['className']}")

                # 再次检查登录表单
                time.sleep(1)
                login_forms = page.locator('input[type="text"], input[type="password"]').all()
                visible_forms = [form for form in login_forms if form.is_visible()]

                if visible_forms:
                    print(f"✅ 成功显示登录对话框！发现 {len(visible_forms)} 个表单元素")
                else:
                    print("❌ 仍没有发现登录表单")

            print("\n=== 最终状态检查 ===")

            # 截图保存最终状态
            screenshot_path = os.path.join(os.getcwd(), 'login_fix_result.png')
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"已保存最终状态截图到: {screenshot_path}")

            # 保存当前页面HTML用于调试
            html_path = os.path.join(os.getcwd(), 'login_fix_final.html')
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(page.content())
            print(f"已保存最终页面HTML到: {html_path}")

        except Exception as e:
            print(f"修复过程中发生错误: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            # 保持浏览器打开10秒供观察
            print("保持浏览器打开10秒供观察...")
            time.sleep(10)
            browser.close()

if __name__ == "__main__":
    login_fix()