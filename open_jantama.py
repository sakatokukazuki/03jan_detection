import pyautogui 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import json
import os


PATH = os.path.dirname(os.path.abspath(__file__))



class OpenJantama():
    # 雀魂へ
    def __init__(self, xpath_list):
        options = Options()
        options.add_experimental_option('detach', True)
        self.driver = webdriver.Chrome(options=options)
        self.driver.get('https://game.mahjongsoul.com/index.html')
        self.driver.maximize_window()
        self.xpath = xpath_list
        self.driver.implicitly_wait(20)

    # 雀魂ログイン
    def _login_jantama(self, mail_address, password):
        # gmailでログイン
        pyautogui.moveTo(1300, 850, duration=17)
        pyautogui.click()

        # address 入力
        self._click(self.xpath["address_box"], interval=1)
        self._send_keys(self.xpath["address_box"], mail_address, interval=1)

        # 次へクリック
        self._click(self.xpath["next_button"], interval=1)

        # password 入力
        self._click(self.xpath["password_box"], interval=1)
        self._send_keys(self.xpath["password_box"], password, interval=1)

        # 次へクリック
        self._click('//*[@id="passwordNext"]/div/button/span', interval=1)

        # 最後確認
        sleep(14)
        pyautogui.moveTo(1000, 770)
        pyautogui.click()

    def _open_match(self):
        self._click_position(1550, 300, duration=13)
        self._click_position(1500, 800, duration=2)

    def _click_position(self, x, y, duration=0):
        pyautogui.moveTo(x, y, duration)
        pyautogui.click()

    def _send_keys(self, xpath, text, interval=0):
        output = self.driver.find_element(By.XPATH, xpath)
        output.send_keys(text)
        sleep(interval)

    def _click(self, xpath, interval=0):
        button = self.driver.find_element(By.XPATH, xpath)
        button.click()
        sleep(interval)


if __name__ == "__main__":

    with open(f'{PATH}/secret.json', 'r') as f:
        user_data = json.load(f)
    
    # xpathjsonを開く
    with open(f'{PATH}/xpath.json', 'r') as f:
        xpath_list = json.load(f)

    openjantama = OpenJantama(xpath_list)
    openjantama._login_jantama(user_data["mail_address"], user_data["password"])
