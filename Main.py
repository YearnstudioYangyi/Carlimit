import json
import datetime
import tkinter as tk
from tkinter import ttk, messagebox
# 作者：2027级高一二十班阳毅


# 数据源
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
    # 其他城市...
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

# 创建主窗口
root = tk.Tk()
root.title("车牌限号查询")

# 设置窗口大小
root.geometry("300x150")
root.resizable(False, False)

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
