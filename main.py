# -- coding: utf-8 --
# @Author: MSCopilot
# @Time: 2025/8/23 21:58
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import shutil
import os
import sys
import json
import pystray
from PIL import Image
import threading

def MoveFile(src: str, dst: str) -> None:
    if not os.path.exists(dst):
        global tray_icon
        print(f"要移动的目录 {dst} 不存在！")
        tray_icon.notify(f"目标目录 {dst} 不存在！", title="移动失败")
        return

    if os.path.isfile(src) and os.path.exists(src):
        file_name = src.split(os.path.sep)[-1]
        time.sleep(0.5)
        dst_path = os.path.join(dst, file_name)  # 构造完整目标路径
        while os.path.exists(dst_path):  # 检查目标文件是否存在
            new_file_name = f"{os.path.splitext(file_name)[0]}-2{os.path.splitext(file_name)[1]}"  # 生成新文件名（如 a.jpg -> a-2.jpg）
            new_src_path = src.replace(file_name, new_file_name)  # 新目标路径
            os.rename(src, new_src_path)  # 重命名源文件
            file_name = new_file_name  # 更新文件名
            src = new_src_path
            dst_path = os.path.join(dst, file_name)
        shutil.move(src, dst)  # 移动文件（此时目标路径无同名文件）

# 先定义事件处理函数
def on_clicked(icon, item):
    global config, tray_icon  # 确保能访问全局变量

    if item.text == "打开 Config 文件":
        import subprocess
        subprocess.Popen(['notepad.exe', 'config.json'])
    elif item.text == "重新加载 Config 文件":
        # 重新加载配置并更新托盘图标
        new_config = load_config(config, "无效的 config.json！")
        if new_config != config:  # 如果配置有变化
            config = new_config
            tray_icon.notify("配置已重新加载", "WatchFile")
    elif item.text == "退出(Quit)":
        icon.stop()
        sys.exit(0)


# 然后定义配置加载函数
def load_config(default=None, notify="无法识别 config.json 文件！"):
    if default is None:
        default = {"FileLib": {}, "WatchDir": []}

    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config_string = f.read().replace(r"{HOME}", os.path.expanduser("~").replace("\\", "\\\\"))

        return json.loads(config_string)

    except Exception as e:
        print(f"\033[1;31m配置加载错误: {str(e)}\033[0m")
        if 'tray_icon' in globals():  # 确保托盘图标已存在
            tray_icon.notify(notify, "WatchFile")
        return default


# 初始化配置
config = load_config()

# 最后创建托盘图标（此时on_clicked已定义）
icon_image = Image.open("icon.png")
menu = (
    pystray.MenuItem("打开 Config 文件", on_clicked),
    pystray.MenuItem("重新加载 Config 文件", on_clicked),
    pystray.Menu.SEPARATOR,
    pystray.MenuItem("退出(Quit)", on_clicked),
)

tray_icon = pystray.Icon("WatchFile", icon_image, "WatchFile", menu)


# 启动托盘图标（可选）
# tray_icon.run()

def background_task():
    pass

def start_tray():
    thread = threading.Thread(target=background_task, daemon=True)  # 守护线程，主程序退出时自动结束
    thread.start()
    tray_icon.run()

Filelib = config["FileLib"]
WatchDir = config["WatchDir"]

#
# Filelib = {
#     (".jpg", ".jpeg", ".png", ".gif", ".bmp"): "C:/Users/ASUS/Pictures",
#     (".mp4", ".avi", ".mkv"): "C:/Users/ASUS/Videos",
#     ("setup.exe", "installer.exe"): "C:/Users/ASUS/Documents/Setups & Installers",
#     (".pdf"): "C:/Users/ASUS/Documents/PDFs",
#     (".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".odt"): "C:/Users/ASUS/Documents",
#     (".mp3", ".m4a", ".wav", ".aac"): "C:/Users/ASUS/Music",
#     (".py", ".pyc", "python"): "C:/Users/ASUS/Documents/Python",
# }

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            for i in Filelib.items():
                for j in i[1]:
                    if j.lower().startswith(".") and event.src_path.lower().endswith(j):
                        if os.path.exists(event.src_path):
                            print(f"匹配到扩展名规则：{j} -> 目标路径：{i[0]}")
                            MoveFile(event.src_path, i[0])
                    elif j.lower() in event.src_path.lower():
                        if os.path.exists(event.src_path):
                            print(f"匹配到扩展名规则：{j} -> 目标路径：{i[0]}")
                            MoveFile(event.src_path, i[0])


observer = Observer()
event_handler = Handler()

for i in range(len(WatchDir)):
    observer.schedule(event_handler, path=WatchDir[i], recursive=True)

observer.start()

print("WatchFile Observer Started...")
print("\nNow Watching:\033[1m")
for i in WatchDir:
    print(i)
print("\033[0m")

start_tray()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()