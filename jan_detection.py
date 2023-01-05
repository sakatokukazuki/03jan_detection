import cv2
import numpy as np
import os
import glob
import win32gui
import win32.lib.win32con as win32con
import pyautogui
from time import sleep
import keyboard


class JanDetection():
    def __init__(self):
        self.PATH = os.path.dirname(os.path.abspath(__file__))
        # 条件に合うファイルパス情報をすべて取得
        file_list = glob.glob(
            f'{self.PATH}/tiles_images/**/*.*', recursive=True)
        pon_list = glob.glob(
            f'{self.PATH}/pon/**/*.*', recursive=True)
        # パス情報からファイル名だけを取り出す
        self.hai_list = [os.path.splitext(os.path.basename(file))[
            0] for file in file_list]

        self.pons = [os.path.splitext(os.path.basename(pons))[
            0] for pons in pon_list]
        # 牌のx座標
        self.hai_x = [429, 493, 573, 642, 711, 781,
                      866, 926, 1023, 1168, 1239, 1305, 1406]

    # 誤検出を減らすため画像を自分の牌だけトリミング
    def _cut(self):
        self.x = 850
        self.y = 380
        self.im = cv2.imread(f'{self.PATH}/data/2023-01-03.png')
        self.im_crop = self.im[850: 1020, 300: 1700]
        self.im_crop2 = self.im[850: 1020, 800: 1700]

    # テンプレートマッチング
    def _matching(self):

        # 画像の読み込み + グレースケール化
        img_gray = cv2.cvtColor(self.im_crop, cv2.COLOR_BGR2GRAY)

        self.loc_list = []
        self.hai_loc = []
        self.hais = []

        for hai_name in self.hai_list:
            template = cv2.imread(f'{self.PATH}/tiles_images/{hai_name}.png')
            template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

            # 処理対象画像に対して、テンプレート画像との類似度を算出する
            res = cv2.matchTemplate(
                img_gray, template_gray, cv2.TM_CCOEFF_NORMED)

            # 閾値を牌によって変更
            if hai_name == "sha":
                threshold = 0.983

            elif hai_name == "hatsu":
                threshold = 0.978

            elif hai_name == "9wan":
                threshold = 0.975

            elif hai_name == "8so" or hai_name == "2pin" or hai_name == "7pin":
                threshold = 0.97

            elif hai_name == "4so":
                threshold = 0.966

            elif hai_name == "1so" or hai_name == "6so" or hai_name == "5so":
                threshold = 0.957

            elif hai_name == "4pin" or hai_name == "8pin":
                threshold = 0.95

            elif hai_name == "5pin":
                threshold = 0.943

            elif hai_name == "9so" or hai_name == "9pin":
                threshold = 0.94

            elif hai_name == "6pin":
                threshold = 0.935

            elif hai_name == "haku":
                threshold = 0.987

            elif hai_name == "ton" or "nan":
                threshold = 0.985

            else:
                threshold = 0.98

            self.loc = np.where(res >= threshold)
            self.hai_loc.append(self.loc)
            self.loc_list.append(f"{hai_name}:{len(self.loc[0])}")
            self.hais.append(len(self.loc[0]))

            # テンプレートマッチング画像の高さ、幅を取得する
            h, w = template_gray.shape
            # 検出した部分に赤枠をつける
            for pt in zip(*self.loc[::-1]):
                cv2.rectangle(self.im_crop, pt,
                              (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

        # 国士無双
        self.kokushi_list = self.hais[0:3] + self.hais[18:]
        # 九蓮筒子
        self.churen_list = self.hais[0:4:3] + \
            self.hais[5:11:2] + self.hais[12:19:2]
        # 索子
        self.churen_so = self.hais[1:5:3] + \
            self.hais[6:11:2] + self.hais[13:20:2]
        # 字牌
        self.jihai = self.hais[21:]
        # print(self.jihai)
        # print(self.loc_list)

    def _pon_matching(self):
        # 画像の読み込み + グレースケール化
        img_gray = cv2.cvtColor(self.im_crop2, cv2.COLOR_BGR2GRAY)

        self.po = []
        self.po_loc = []
        self.po_len = []
        self.po_num = []

        for pon in self.pons:
            template_pon = cv2.imread(f'{self.PATH}/pon/{pon}.png')
            template_pon_gray = cv2.cvtColor(template_pon, cv2.COLOR_BGR2GRAY)

            # 処理対象画像に対して、テンプレート画像との類似度を算出する
            res = cv2.matchTemplate(
                img_gray, template_pon_gray, cv2.TM_CCOEFF_NORMED)

            if pon == "haku":
                threshold = 0.99
            else:
                threshold = 0.8

            self.po = np.where(res >= threshold)
            self.po_loc.append(self.po)
            self.po_num.append(len(self.po[0]))
            for i in range(len(self.po_num)):
                if self.po_num[i] > 0:
                    self.po_num[i] = 3
            self.po_len.append(f"{pon}:{self.po_num[-1]}")
            # テンプレートマッチング画像の高さ、幅を取得する
            h, w = template_pon_gray.shape
            # 検出した部分に赤枠をつける
            for pt in zip(*self.po[::-1]):
                cv2.rectangle(self.im_crop2, pt,
                              (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
            # 画像の保存(確認用)
            cv2.imwrite('./tpl_match_after.png', self.im_crop)

        # print(self.po_len)
    def _judge(self):
        # 国士無双判定
        kokushi = self.kokushi_list.count(1) + self.kokushi_list.count(2)*2
        if kokushi == 14:
            print("国士無双")
        
        # else:
        #     print(f"国士無双まで{self.kokushi_list.count(0)}枚")

        # 四暗刻判定
        anko = self.hais.count(3)
        atama = self.hais.count(2)
        if anko == 4 and atama == 1:
            print("四暗刻")
        
        # elif anko == 4 and atama == 0:
        #     print("四暗刻単騎聴牌")
        # else:
        #     print(f"{anko}暗刻")

        # 九蓮宝燈判定
        churen = [3,1,1,1,1,1,1,1,3]
        dif_so = [0]*9
        dif = [0]*9
        for i in range(9):
            dif[i] = self.churen_list[i] - churen[i]
            dif_so[i] = self.churen_so[i] - churen[i]
        if dif.count(0) == 8 and dif.count(1) == 1:
            print("九蓮宝燈(筒子)")
        elif dif_so.count(0) == 8 and dif_so.count(1) == 1:
            print("九蓮宝燈(索子)")

        # 順子カウント
        jun_count = 0
        jun = [0]*6
        jun_list = [0]*7
        for i in range(7):
            jun_list[i] = jun[:i] + [1,1,1] + jun[i:]
            if jun_list[i] == self.churen_list or jun_list[i] == self.churen_so:
                jun_count+=1

        # 小四喜
        # 1暗刻or1順子+方角により判定
        hogaku_pon = [self.po_num[-3], 0, self.po_num[-2], self.po_num[-1]]
        a = hogaku_pon + self.hais[-4:]
        if (jun_count == 1 and self.hais[:20].count(3) == 0) or (jun_count == 0 and self.hais[:20].count(3) == 1):
            if a.count(3) == 3 and a.count(2) == 1:
                print("小四喜")

        #大三元
        #1雀頭+1暗刻or1順子 + 三元牌
        daisan = [0]*3
        if atama == 1:
            if (jun_count == 1 ) or (self.hais[:-8].count(3) + self.hais[-4:].count(3) + self.po_num[-3:].count(3) + self.po_num[:-6].count(3) == 1):
                for i in range(3):
                    daisan[i] = self.hais[-7+i] + self.po_num[-6+i]
                if daisan == [3,3,3]:
                    print("大三元")

        #字一色
        tsuiso = [0]*7
        for i in range(4):
            tsuiso[i] = self.jihai[i] + self.po_num[-6+i]
        tsuiso[4] = self.jihai[4]
        for i in range(5,7):
            tsuiso[i] = self.jihai[i] + self.po_num[-6+i]

        if tsuiso.count(3) == 4 and tsuiso.count(2):
            print("字一色")

    def _screenshot(self):
        jantama = win32gui.FindWindow(None, 'jantama')
        win32gui.SetForegroundWindow(jantama)
        win32gui.ShowWindow(jantama, win32con.SW_MAXIMIZE)
        sleep(1)
        s = pyautogui.screenshot()
        s.save('screenshot1.png')

    def _click(self):
        while True:
            pyautogui.click(self.hai_x[0], 1000, button="left", clicks=2)
            sleep(3)
            if keyboard.is_pressed("a"):
                break

    def _select(self):
        for i in range(len(self.hai_loc)):
            print(self.hai_loc[i][0], self.hai_loc[i][1])



if __name__ == "__main__":

    jan_detection = JanDetection()
    # jan_detection._screenshot()
    jan_detection._cut()
    jan_detection._matching()
    jan_detection._pon_matching()
    jan_detection._judge()
    # jan_detection._click()
    # jan_detection._select()
