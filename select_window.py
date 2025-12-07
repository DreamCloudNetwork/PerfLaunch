#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/12/7 21:11
# @Author  : Kevin Chang
# @File    : select_window.py
# @Software: PyCharm
import tkinter as tk
from tkinter import ttk
from typing import List, Callable, Any

class MaterialSelectWindow:
    def __init__(self, list_items: List[str], callback: Callable[[Any], None], title: str = "Select Item"):
        self.item_labels = None
        self.style = None
        self.main_frame = None
        self.items = list_items
        self.callback = callback
        self.selected_index = 0

        # 创建主窗口
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("400x300")
        self.root.configure(bg="#f5f5f5")

        # 设置窗口样式
        self.setup_styles()
        self.create_widgets()
        self.bind_events()

        # 初始化选择状态
        self.update_selection()

    def setup_styles(self):
        """设置Material Design样式"""
        self.style = ttk.Style()
        self.style.configure("Material.TFrame", background="#ffffff")
        self.style.configure("Material.TLabel", background="#ffffff", foreground="#212121",
                             font=("Roboto", 12))
        self.style.configure("Selected.TLabel", background="#e3f2fd", foreground="#1976d2",
                             font=("Roboto", 12, "bold"))

    def create_widgets(self):
        """创建界面组件"""
        # 主容器
        self.main_frame = ttk.Frame(self.root, style="Material.TFrame")
        self.main_frame.pack(fill="both", expand=True, padx=16, pady=16)

        # 创建列表项
        self.item_labels = []
        for i, item in enumerate(self.items):
            label = ttk.Label(self.main_frame, text=item, style="Material.TLabel",
                              padding=(16, 12), cursor="hand2")
            label.pack(fill="x", pady=2)
            label.bind("<Button-1>", lambda e, idx=i: self.on_item_click(idx))
            self.item_labels.append(label)

        # 底部按钮区域
        button_frame = ttk.Frame(self.main_frame, style="Material.TFrame")
        button_frame.pack(side="bottom", fill="x", pady=(16, 0))

        cancel_btn = tk.Button(button_frame, text="取消", command=self.cancel,
                               bg="#f5f5f5", fg="#616161", relief="flat",
                               font=("Roboto", 10), cursor="hand2")
        cancel_btn.pack(side="right", padx=(8, 0))

        confirm_btn = tk.Button(button_frame, text="确认", command=self.confirm,
                                bg="#2196f3", fg="white", relief="flat",
                                font=("Roboto", 10, "bold"), cursor="hand2")
        confirm_btn.pack(side="right")

        button_frame.pack_forget()

    def bind_events(self):
        """绑定键盘事件"""
        self.root.bind("<Up>", self.move_up)
        self.root.bind("<Down>", self.move_down)
        self.root.bind("<Return>", lambda e: self.confirm())
        self.root.bind("<Escape>", lambda e: self.cancel())
        self.root.focus_set()

    def update_selection(self):
        """更新选择状态显示"""
        for i, label in enumerate(self.item_labels):
            if i == self.selected_index:
                label.configure(style="Selected.TLabel")
                label.configure(background="#e3f2fd")  # 滚动到可视区域
                label.update_idletasks()
            else:
                label.configure(style="Material.TLabel")
                label.configure(background="#ffffff")

    def move_up(self, event=None):
        """向上移动选择"""
        if self.selected_index > 0:
            self.selected_index -= 1
            self.update_selection()
        str(event)

    def move_down(self, event=None):
        """向下移动选择"""
        if self.selected_index < len(self.items) - 1:
            self.selected_index += 1
            self.update_selection()
        str(event)

    def on_item_click(self, index):
        """点击项目"""
        self.selected_index = index
        self.update_selection()
        self.confirm()

    def confirm(self):
        """确认选择"""
        selected_item = self.items[self.selected_index]
        self.root.destroy()
        if self.callback:
            self.callback(selected_item)

    def cancel(self):
        """取消选择"""
        self.root.destroy()
        if self.callback:
            self.callback(None)

    def show(self):
        """显示窗口"""
        self.root.mainloop()

# 使用示例
def example_callback(selected_item):
    if selected_item:
        print(f"选择了: {selected_item}")
    else:
        print("取消选择")

# 创建并显示选择窗口
if __name__ == "__main__":
    items = ["选项一", "选项二", "选项三", "选项四", "选项五"]
    window = MaterialSelectWindow(items, example_callback, "请选择一个选项")
    window.show()
