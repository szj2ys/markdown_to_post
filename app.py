# *_*coding:utf-8 *_*
# @Author: SZJ
from __future__ import absolute_import, division, print_function
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import uvicorn

app = FastAPI()

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)

# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
resources_dir = os.path.join(current_dir, "resources")

# 挂载静态文件目录
app.mount("/", StaticFiles(directory=resources_dir), name="static")

class ResourceChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        print(f"Detected change in resources: {event.src_path}")
        # 这里可以添加任何您想在文件变化时执行的操作
        # 例如，重新加载特定的路由或更新缓存

# 设置文件系统监视器
event_handler = ResourceChangeHandler()
observer = Observer()
observer.schedule(event_handler, resources_dir, recursive=True)
observer.start()

if __name__ == "__main__":
    print(f"Resources directory: {resources_dir}")
    uvicorn.run(app, port=8999)
