from selenium import webdriver
import time
import datetime
from selenium.webdriver.common.by import By

# 打开Chrome浏览器
browser = webdriver.Chrome()


def login():
    # 打开淘宝首页，通过扫码登录
    global browser
    browser.get("https://www.taobao.com")
    time.sleep(3)

    if browser.find_element(By.NAME, "亲，请登录"):
        browser.find_element(By.NAME, "亲，请登录").click()
        print(f"请尽快扫码登录")
        time.sleep(30)


def picking(method):
    # 打开购物车列表页面
    browser.get("https://cart.taobao.com/cart.htm")
    time.sleep(3)
    # 是否全选购物车
    if method == 0:
        while True:
            try:
                if browser.find_element(By.ID, 'J_SelectAll1'):
                    browser.find_element(By.ID, 'J_SelectAll1').click()
                    break
            except:
                print(f"找不到购买按钮")
    if method == 1:
        print(f"请手动勾选需要购买的商品")
        time.sleep(15)


def buy(times):
    while True:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        print(now)
        # 对比时间，时间到的话就点击结算
        if now > times:
            # 点击结算按钮
            while True:
                try:
                    if browser.find_element(By.LINK_TEXT, '结 算'):
                        browser.find_element(By.LINK_TEXT, '结 算').click()
                        print(f"结算成功")
                        break
                except:
                    pass
            # 点击提交订单按钮
            while True:
                try:
                    if browser.find_element(By.LINK_TEXT, '提交订单'):
                        browser.find_element(By.LINK_TEXT, '提交订单').click()
                        print(f"抢购成功，请尽快付款")
                except:
                    print(f"再次尝试提交订单")
                    pass
            time.sleep(0.01)


if __name__ == '__main__':
    picking(1)
    buy("2022-08-28 11:33:00.000000")