from pynput import mouse #module pynputをインポート
import pyautogui #module pyautoguiをインポート 

#マウスイベントハンドラを定義
def on_move(x, y):
    return

def on_click(x, y, button, pressed):
    if pressed:
        # Stop listener
        return False

def on_scroll(x, y, dx, dy):
    return

#リスナー起動
#Collect events until released
with mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll) as listener:
    listener.join()

recttop_x, recttop_y = pyautogui.position()
print('Pointer cliked at {0}'.format(
        (recttop_x, recttop_y)))

#クリックした座標を表示
print('recttop_x = ', recttop_x)
print('recttop_y = ', recttop_y)