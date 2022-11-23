import cv2
import numpy as np
import os
import glob

class JanDetection():
    def __init__(self):
        self.PATH = os.path.dirname(os.path.abspath(__file__))
        # 条件に合うファイルパス情報をすべて取得
        file_list = glob.glob(f'{self.PATH}/tiles_images/**/*.*', recursive=True)
        # パス情報からファイル名だけを取り出す
        self.hai_list = [os.path.splitext(os.path.basename(file))[0] for file in file_list]

    # 画像を自分の牌だけトリミング
    def cut(self):
        self.im = cv2.imread(f'{self.PATH}/data/data1.png')
        self.im_crop = self.im[900 : 1020,380 : 1450]

    # テンプレートマッチング
    def matching(self):

        # 画像の読み込み + グレースケール化
        img_gray = cv2.cvtColor(self.im_crop, cv2.COLOR_BGR2GRAY)
        for hai_name in self.hai_list:
            template = cv2.imread(f'{self.PATH}/tiles_images/{hai_name}.png')
            template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

            # 処理対象画像に対して、テンプレート画像との類似度を算出する
            res = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)

            # 類似度の高い部分を検出する
            threshold = 0.9
            loc = np.where(res >= threshold)
            print(len(loc[0]))

            # テンプレートマッチング画像の高さ、幅を取得する
            h, w = template_gray.shape
            # 検出した部分に赤枠をつける
            for pt in zip(*loc[::-1]):
                cv2.rectangle(self.im_crop, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

            # 画像の保存
            cv2.imwrite('./tpl_match_after.png', self.im_crop)


if __name__ == "__main__":

    jan_detection = JanDetection()
    jan_detection.cut()        
    jan_detection.matching()
