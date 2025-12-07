import tkinter as tk
from PIL import Image, ImageDraw
import pystray
import threading
from select_window import MaterialSelectWindow
from main import apps
import os

# 应用列表

def create_image():
    """创建托盘图标图像"""
    # 创建一个简单的图标
    width = 64
    height = 64
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    dc = ImageDraw.Draw(image)
    # 绘制一个蓝色圆圈作为图标
    dc.ellipse((10, 10, width-10, height-10), fill=(0, 123, 255, 255))
    # 绘制一个白色方块
    dc.rectangle(
        (width // 2 - 5, height // 2 - 5, width // 2 + 5, height // 2 + 5),
        fill=(255, 255, 255, 255))
    return image

def launch_app(app_name):
    """启动应用程序"""
    if not app_name:
        return
    print(f"Launching {apps[app_name]}...")
    os.popen(f"exec {apps[app_name]}", mode='r', buffering=-1)

def show_select_window(icon, item):
    """显示选择窗口"""
    def run_window():
        # 在主线程中创建并显示窗口
        window = MaterialSelectWindow(list(apps.keys()), launch_app, "请选择一个选项")
        window.show()
    
    # 在新线程中运行窗口，避免阻塞托盘图标
    window_thread = threading.Thread(target=run_window, daemon=True)
    window_thread.start()

def exit_program(icon, item):
    """退出程序"""
    icon.stop()
    os._exit(0)  # 强制退出程序

def start_tray_icon():
    """启动托盘图标"""
    # 创建菜单
    menu = pystray.Menu(
        pystray.MenuItem("打开选择窗口", show_select_window),
        pystray.MenuItem("退出", exit_program)
    )
    
    # 创建图标
    icon = pystray.Icon("PerfLaunch", create_image(), "PerfLaunch", menu)
    
    # 在独立线程中运行图标
    icon.run()

def main():
    """主函数"""
    # 启动托盘图标
    start_tray_icon()

if __name__ == "__main__":
    main()