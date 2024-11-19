import json
import datetime
import os
import tkinter as tk
from tkinter import ttk, messagebox
import requests

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

def auto_choice_city(car):
    li = {'京A':'北京','沪A':'上海'}
    if li.get(car[0:2]) != None:
        return li.get(car[0:2])
    else:
        return -1

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
    if disable_checkbox_var.get():
        temp = auto_choice_city(plate_number)
        if temp == -1:
            messagebox.showwarning("警告", "无法自动匹配，请手动选择")
            return
        else:
            city = temp
    if not city or not plate_number:
        messagebox.showwarning("警告", "城市或车牌号为空")
        return
    result = check_limitation(city, plate_number, data)
    messagebox.showinfo("限号情况", result)

def load_local_data():
    if os.path.exists("./data.json"):
        with open("./data.json", "r", encoding='utf-8') as f:
            global data  # 使用全局变量 data
            data = json.load(f)
    else:
        messagebox.showerror("错误", "本地数据文件不存在")
        return -1
    
    # 更新下拉框的城市选项
    city_entry['values'] = list(data.keys())
    
    messagebox.showinfo("提示", "已从本地读取数据")
    update_status("已从本地读取数据")
    return data

def sync_from_network():
    try:
        # 发送网络请求
        response = requests.get("https://db.yearnstudio.cn/api/data")
        
        # 检查请求是否成功
        if response.status_code == 200:
            # 解析 JSON 数据
            new_data = response.json()
            
            # 更新全局变量 data
            global data
            data = new_data
            
            # 更新下拉框的城市选项
            city_entry['values'] = list(data.keys())
            
            # 更新状态标签
            update_status("已从网络同步数据")
            messagebox.showinfo("提示", "已从网络同步数据")
        else:
            messagebox.showerror("错误", f"网络请求失败")
    except Exception as e:
        messagebox.showerror("错误", f"网络请求发生错误: {str(e)}")

def about():
    # 关于信息
    messagebox.showinfo("关于", "这是一个车牌限号查询工具\n由yangyi制作")

def toggle_city_entry(var):
    if var.get():
        city_entry.config(state=tk.DISABLED)
    else:
        city_entry.config(state=tk.NORMAL)

def exit_app():
    # 退出应用
    root.quit()

# 创建主窗口
root = tk.Tk()
root.title("车牌限号查询")

# 设置窗口大小
window_width = 300
window_height = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 计算窗口在屏幕上的中心位置
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

# 设置窗口的位置和大小
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# 禁用窗口大小调整
root.resizable(False, False)
root.wm_iconbitmap('')

# 其他代码保持不变

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

# 底部标签
# status_label = tk.Label(root, text="当前使用的是示例数据，请从同步选项进行同步")
# status_label.grid(row=4, column=0, columnspan=2,pady=5)

# 定义一个函数来更新 Label 的内容
def update_status(message):
    status_label.config(text=message)

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

# 创建自动匹配选项
disable_checkbox_var = tk.BooleanVar()
disable_checkbox = tk.Checkbutton(root, text="自动匹配", variable=disable_checkbox_var, command=lambda: toggle_city_entry(disable_checkbox_var))
disable_checkbox.grid(row=2, column=0, columnspan=2, pady=5)  # 将行参数设置为2

# 创建提交按钮
submit_button = tk.Button(root, text="查询", command=on_submit)
submit_button.grid(row=3, column=0, columnspan=2, pady=10)  # 将行参数设置为3

# 底部标签
status_label = tk.Label(root, text="当前使用的是示例数据，请从同步选项进行同步", fg="blue")
status_label.grid(row=4, column=0, columnspan=2, pady=5) 

# 运行主循环
root.mainloop()
