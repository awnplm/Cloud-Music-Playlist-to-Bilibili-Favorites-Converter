# -*- coding: utf-8 -*-
"""
功能：自动登录B站 → 搜索歌曲 → 收藏到指定收藏夹
优化：所有 find_element 改为 WebDriverWait 等待版本（上限10秒）
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
import base64
import json
import requests
import pyautogui
import keyboard
from time import sleep

# 全局配置
tabs = 0
CDriverPath = r""
sspath = r""
tlusername = ""
tlpassword = ""
tlId = "08272733"
username = ""
password = ""
userpath = r""
favoritesName=""
song="nothing"

# -----------------------------
# 启动浏览器
# -----------------------------
def boot():
    q1 = Options()
    q1.add_argument(r"user-data-dir=D:\system\selenium_profile")
    q1.add_argument("--no-sandbox")
    q1.add_argument("--disable-dev-shm-usage")
    q1.add_argument("--remote-debugging-port=9222")
    q1.add_experimental_option("detach", True)  # 浏览器不随程序结束而关闭

    a1 = webdriver.Chrome(service=Service(CDriverPath), options=q1)
    a1.get("https://www.bilibili.com/")
    a1.maximize_window()
    return a1

# -----------------------------
# 调用图灵验证码识别API
# -----------------------------
def b64_api(username, password, img_path, ID):
    with open(img_path, 'rb') as f:
        b64_data = base64.b64encode(f.read())
    b64 = b64_data.decode()
    data = {"username": username, "password": password, "ID": ID, "b64": b64, "version": "3.1.1"}
    data_json = json.dumps(data)
    result = json.loads(requests.post("http://www.fdyscloud.com.cn/tuling/predict", data=data_json).text)
    return result

# -----------------------------
# 登录时风险验证
# -----------------------------
def loginRisk(bi):
    name = time.strftime("%Y%m%d_%H%M%S") + '.png'
    sleep(1)

    captcha = WebDriverWait(bi, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "geetest_panel_next"))
    )
    sleep(1)
    captcha.screenshot(rf"{sspath}\{name}")

    verificationCode = b64_api(username=tlusername, password=tlpassword, img_path=rf".\screenshot\{name}", ID=tlId)

    for key, value in verificationCode["data"].items():
        x, y = int(value["X坐标值"]) + 792, int(value["Y坐标值"]) + 383
        pyautogui.moveTo(x, y)
        pyautogui.click()
        sleep(1)

    commit = WebDriverWait(bi, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "geetest_commit"))
    )
    commit.click()

# -----------------------------
# 登录逻辑
# -----------------------------
def login(bi):
    WebDriverWait(bi, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "header-login-entry"))
    ).click()
    sleep(1)

    WebDriverWait(bi, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "form__item"))
    ).click()
    sleep(1)

    WebDriverWait(bi, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@placeholder='请输入账号']"))
    ).send_keys(username)

    WebDriverWait(bi, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@placeholder='请输入密码']"))
    ).send_keys(password)

    WebDriverWait(bi, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "btn_primary "))
    ).click()

    loginRisk(bi)
    sleep(2)

    WebDriverWait(bi, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "risk-input-after-active"))
    ).click()

    sleep(1)
    loginRisk(bi)

# -----------------------------
# 标签页切换函数
# -----------------------------
def switchNewTab(bi):
    global tabs
    tabs += 1
    handles = bi.window_handles
    bi.switch_to.window(handles[tabs])

def switchOldTab(bi):
    global tabs
    if tabs > 0:
        tabs -= 1
        bi.close()
        handles = bi.window_handles
        bi.switch_to.window(handles[tabs])
    else:
        print("only one tab\n")

# -----------------------------
# 搜索并收藏歌曲
# -----------------------------
def searchSong(bi):
    before = None
    global tabs,song

    with open("songData.json", "r", encoding="utf-8") as f:
        songs = json.load(f)

    flag = True
    try:
        for song in songs:
            if flag:
                # 首页搜索框
                search = WebDriverWait(bi, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "nav-search-input"))
                )
                search.click()
                search.send_keys(f"{song['name']} {song['artist']}")
                WebDriverWait(bi, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "nav-search-btn"))
                ).click()
                switchNewTab(bi)
            else:
                # 搜索结果页搜索框
                search = WebDriverWait(bi, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "search-input-el"))
                )
                search.click()
                sleep(1)
                keyboard.press_and_release('ctrl+a')
                time.sleep(0.1)
                keyboard.press_and_release('backspace')
                search.send_keys(f"{song['name']} {song['artist']}")
                WebDriverWait(bi, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "search-button"))
                ).click()

            sleep(3)

            video = WebDriverWait(bi, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "bili-video-card"))
            )
            url = video.find_element(By.TAG_NAME, "a").get_attribute("href")

            bi.execute_script("window.open(arguments[0]);", url)
            bi.switch_to.window(bi.window_handles[-1])
            switchNewTab(bi)

            sleep(4)

            WebDriverWait(bi, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//*[contains(@class, 'video-fav') and contains(@class, 'video-toolbar-left-item')]"
                ))
            ).click()

            favor = WebDriverWait(bi, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "group-list"))
            )

            WebDriverWait(bi, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    f"//label[span[@title='{favoritesName}' and contains(@class,'fav-title')]]"
                ))
            ).click()

            WebDriverWait(bi, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//*[contains(@class, 'btn') and contains(@class, 'submit-move')]"
                ))
            ).click()

            sleep(1)
            switchOldTab(bi)
            flag = False
            before = song

    except Exception as e:
        with open("now search song.json", "w", encoding="utf-8") as f:
            f.write(str(song))
        print("❌ 出错：", e)

# -----------------------------
# 主程序入口
# -----------------------------
bi = boot()
# login(bi)
# input("请在浏览器中完成登录后按 Enter 继续...")
searchSong(bi)
