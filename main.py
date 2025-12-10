import time
import os
from pynput import keyboard
from select_window import MaterialSelectWindow
from config import CustomConfigParser
import threading
import tray_icon

# items = ["选项一", "选项二", "选项三", "选项四", "选项五"]

apps = {"Microsoft Edge":"microsoft-edge-stable"}
trigger_keys = []
parser = CustomConfigParser()
config = parser.parse_file('config.ccf')
for key in parser.get("general","trigger_keys"):
    trigger_keys.append(eval(key))
for app in parser.get("general","apps"):
    apps[app] = parser.get("general","apps")[app]

current_press_keys = []
showing_gui = False

def on_press(key):
    try:
        if key not in current_press_keys:
            print('字母键： {} 被按下'.format(key.char))
            current_press_keys.append(key)
    except AttributeError:
        print('特殊键： {} 被按下'.format(key))
        current_press_keys.append(key)

def on_release(key):
    print('{} 释放了'.format(key))
    current_press_keys.remove(key)

def launch_app(app_name):
    if not app_name:
        return
    print(f"Launching {apps[app_name]}...")
    os.popen(f"exec {apps[app_name]}", mode='r', buffering=-1)

def main():
    global showing_gui
    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()

    # 启动托盘图标
    tray_thread = threading.Thread(target=tray_icon.start_tray_icon, daemon=True)
    tray_thread.start()

    print("Hello from perflaunch!")
    while True:
        time.sleep(0.01)
        # print(f"Currently pressed keys: {current_press_keys}")
        if set(trigger_keys) <= set(current_press_keys):
            if not showing_gui:
                showing_gui = True
                window = MaterialSelectWindow(list(apps.keys()), launch_app, "请选择一个选项")
                window.show()
                showing_gui = False
        else:
            showing_gui = False


if __name__ == "__main__":
    main()