# -*- coding:utf-8 -*-

import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import pymongo


client = pymongo.MongoClient('localhost', 27017)
db = client.db
collection = db.house


class MyHandler(FileSystemEventHandler):

    def on_created(self,event):
        pass

    def on_modified(self,event):
        if not event.is_directory:
            print("检测到生成新文件")
            collection.insert_one(
                    {
                        'path': event.src_path,
                        'content': open(event.src_path, 'r').read()
                        })
            os.remove(event.src_path)
            print("已将新文件放进mongodb")


if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='./www', recursive=True)
    observer.start()
    try:
        print "started myWatch"
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
