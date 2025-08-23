# -- coding: utf-8 --
# @Author: MSCopilot
# @Time: 2025/8/23 21:58

import time
import shutil
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def MoveFile(src: str, dst: str) -> None:
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

Filelib = {
    (".jpg", ".jpeg", ".png", ".gif"): "C:\\Users\\ASUS\\Pictures",
    (".mp4", ".avi"): "C:\\Users\\ASUS\\Videos",
    ("setup.exe", "installer.exe"): "C:\\Users\\ASUS\\Documents\\Setups & Installers",
    (".pdf"): "C:\\Users\\ASUS\\Documents\\PDFs",
    (".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"): "C:\\Users\\ASUS\\Documents",
    (".mp3", ".m4a", ".wav", ".aac"): "C:\\Users\\ASUS\\Music",
}

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            for i in Filelib.keys():
                for j in i:
                    if j.lower().startswith(".") and event.src_path.lower().endswith(j):
                        if os.path.exists(event.src_path):
                            print(f"匹配到扩展名规则：{j} -> 目标路径：{Filelib[i]}")
                            MoveFile(event.src_path, Filelib[i])
                    elif j.lower() in event.src_path.lower():
                        if os.path.exists(event.src_path):
                            print(f"匹配到扩展名规则：{j} -> 目标路径：{Filelib[i]}")
                            MoveFile(event.src_path, Filelib[i])


observer = Observer()
event_handler = MyHandler()
observer.schedule(event_handler, path="C:\\Users\\ASUS\\Downloads", recursive=True)
observer.start()

print("Observer Started...")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()