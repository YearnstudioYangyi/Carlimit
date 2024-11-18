import json
import datetime
import os
import tkinter as tk
from tkinter import ttk, messagebox

# 作者：2027级高一二十班阳毅
data = {
    "北京": {
        "周一": ["1", "6"],
        "周二": ["2", "7"],
        "周三": ["3", "8"],
        "周四": ["4", "9"],
        "周五": ["5", "0"],
    },
    "上海": {
        "周一": ["1", "6"],
        "周二": ["2", "7"],
        "周三": ["3", "8"],
        "周四": ["4", "9"],
        "周五": ["5", "0"],
    },
    # 示例数据
}

def check_limitation(city, plate_number, data):
    # 获取当前星期几
    today = datetime.datetime.now().strftime("%A")
    week_days = {
        "Monday": "周一",
        "Tuesday": "周二",
        "Wednesday": "周三",
        "Thursday": "周四",
        "Friday": "周五",
        "Saturday": "周六",
        "Sunday": "周日"
    }
    current_day = week_days[today]

    # 获取当前城市的限号规则
    if city in data and current_day in data[city]:
        allowed_plates = data[city][current_day]
        last_digit = plate_number[-1]  # 获取车牌号的最后一位数字
        if last_digit in allowed_plates:
            return f"今天 {current_day} 在 {city} 车牌号 {plate_number} 限号"
        else:
            return f"今天 {current_day} 在 {city} 车牌号 {plate_number} 不限号"
    else:
        return f"没有找到 {city} 的限号规则"

def on_submit():
    city = city_var.get()
    plate_number = plate_var.get()
    
    if not city or not plate_number:
        messagebox.showwarning("警告", "请输入城市和车牌号")
        return
    
    result = check_limitation(city, plate_number, data)
    messagebox.showinfo("限号情况", result)

def load_local_data():
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            data = json.load(f)
    else:
        messagebox.showerror("错误", "本地数据文件不存在")
        return -1
    messagebox.showinfo("提示", "已从本地读取数据")
    return data

def sync_from_network():
    # 从网络同步数据的逻辑
    messagebox.showinfo("提示", "正在开发")

def about():
    # 关于信息
    messagebox.showinfo("关于", "这是一个车牌限号查询工具\n由yangyi制作")

def exit_app():
    # 退出应用
    root.quit()

# 创建主窗口
root = tk.Tk()
root.title("车牌限号查询")

# 设置窗口大小
root.geometry("300x150")
root.resizable(False, False)

# 创建菜单栏
menu_bar = tk.Menu(root)

# 创建文件菜单
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="本地读取", command=load_local_data)
file_menu.add_command(label="从网络同步", command=sync_from_network)
menu_bar.add_cascade(label="同步", menu=file_menu)

# 创建帮助菜单
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="关于", command=about)
help_menu.add_command(label="退出", command=exit_app)
menu_bar.add_cascade(label="帮助", menu=help_menu)

# 将菜单栏添加到窗口
root.config(menu=menu_bar)

# 创建标签
tk.Label(root, text="城市:").grid(row=0, column=0, padx=10, pady=5)
tk.Label(root, text="车牌号:").grid(row=1, column=0, padx=10, pady=5)

# 创建输入框
city_var = tk.StringVar()
plate_var = tk.StringVar()

# 初始化下拉框的选项
city_entry = ttk.Combobox(root, textvariable=city_var, values=list(data.keys()))
city_entry.grid(row=0, column=1, padx=10, pady=5)

plate_entry = tk.Entry(root, textvariable=plate_var)
plate_entry.grid(row=1, column=1, padx=10, pady=5)

# 创建提交按钮
submit_button = tk.Button(root, text="查询", command=on_submit)
submit_button.grid(row=2, column=0, columnspan=2, pady=10)

# 运行主循环
root.mainloop()
