import cv2
import pyautogui as pg
import numpy as np
import sys
from PyQt5 import QtWidgets
import threading
import time

class Config():
    def __init__(self):
        # パラメータ管理
        self.start_flag = 0
        self.stop_flag = 0
        self.fps = 15
        self.m_time = 10 # s
        self.h, self.w = np.array(pg.screenshot()).shape[:2]
        self.img_list = []

class RecordThread():
    def __init__(self, config):
        super().__init__()
        self.config = config

    def loop(self):
        self.config.img_list = []
        while self.config.stop_flag != 1:
            time.sleep(0.1)
            img = pg.screenshot()
            img = np.array(img)
            img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
            self.config.img_list.append(img)

class CaptureApp(QtWidgets.QWidget):
    def __init__(self):
        super(CaptureApp, self).__init__()
        self.config = Config()

        # layout
        self.hbox_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.hbox_layout)

        # widgetの配置
        self.createWidget()

    # 閉じるボタンをしたときの処理
    def closeEvent(self, event):
        if self.config.start_flag == 1:
            self.config.stop_flag = 1
            self.record_thread.join()

    def createWidget(self):
        # button
        self.start_button = QtWidgets.QPushButton('start')
        self.stop_button = QtWidgets.QPushButton('stop')
        self.label = QtWidgets.QLabel('please start')
        self.hbox_layout.addWidget(self.start_button)
        self.hbox_layout.addWidget(self.stop_button)
        self.hbox_layout.addWidget(self.label)

        # function
        self.start_button.clicked.connect(self.recordStart)
        self.stop_button.clicked.connect(self.recordStop)

    def updateLabel(self):
        if self.config.stop_flag == 0:
            self.label.setText('rec now')
        elif self.config.stop_flag == 1:
            self.label.setText('please start')

    def recordStart(self):
        self.config.start_flag = 1
        self.record_thread = threading.Thread(target = record_control, args = (self.config, ))
        self.record_thread.start()

        # label表示名の更新
        self.updateLabel()

    def recordStop(self):
        # start flagが1の場合
        if self.config.start_flag == 1:
            # stop flagを1にする
            self.config.stop_flag = 1
            # thread処理解除
            self.record_thread.join()
            # 画面録画を保存
            self.recordSave()

            # label表示名の更新
            self.updateLabel()

            # stop flagを0にする
            self.config.stop_flag = 0
            # start flagを0にする
            self.config.start_flag = 0
        else:
            print('please rec start')

    def recordSave(self):
        self.save_path = QtWidgets.QFileDialog.getSaveFileName(self, 'save file', filter = '*.mp4')[0]

        if self.save_path == '':
            return
        fourcc = cv2.VideoWriter_fourcc('m','p','4', 'v')
        video = cv2.VideoWriter(self.save_path, fourcc, self.config.fps, (self.config.w, self.config.h))
        for img in self.config.img_list:
            video.write(img)
        video.release()

def record_control(config):
    rec = RecordThread(config)
    rec.loop()

def main():
    app = QtWidgets.QApplication(sys.argv)
    win = CaptureApp()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()