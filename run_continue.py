import time
import tidevice
import csv

import os
from datetime import datetime

from tools.report import Report
strDate = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
base_path = os.path.dirname(os.path.abspath(__file__))

results_path = os.path.join(base_path, 'results', 'com.yueyou.cyreader')
lists = os.listdir(results_path)         # 列出目录的下所有文件和文件夹保存到lists
lists.sort(key=lambda fn: os.path.getmtime(results_path + "/" + fn))  # 按时间排序
continue_path = os.path.join(results_path, lists[-1])      # 获取最新的文件保存到file_new
# continue_path = os.path.join(base_path, 'results', 'com.yueyou.cyreader', '2022_07_14_15_15_34')
print('当前文件夹下的最新文件夹为', continue_path)

cpu_file = os.path.join(continue_path, 'cpuinfo.csv')
fps_file = os.path.join(continue_path, 'fpsinfo.csv')
memory_file = os.path.join(continue_path, 'memoryinfo.csv')


def new_report(test_report):
    lists = os.listdir(test_report)         # 列出目录的下所有文件和文件夹保存到lists
    lists.sort(key=lambda fn: os.path.getmtime(test_report + "/" + fn)) # 按时间排序
    file_new = os.path.join(test_report, lists[-1])      # 获取最新的文件保存到file_new
    print('当前文件夹下的最新文件夹为', file_new)
    return file_new


def cpu_title_writer():
    # cpu_title = ["datetime", "device_cpu_rate%", "user%", "system%","idle%"]
    cpu_title = ["timestamp", "pid", "device_cpu_rate", "system_cpu_rate", "count"]
    try:
        with open(cpu_file, 'w+') as df:
            csv.writer(df, lineterminator='\n').writerow(cpu_title)
    except RuntimeError as e:
        print(e)


def fps_title_writer():
    fps_title = ['timestamp', 'fps', 'value']
    try:
        with open(fps_file, 'w+') as df:
            csv.writer(df, lineterminator='\n').writerow(fps_title)
    except RuntimeError as e:
        print(e)


def memory_title_writer():
    memory_title = ['timestamp', 'pid', 'value']
    try:
        with open(memory_file, 'w+') as df:
            csv.writer(df, lineterminator='\n').writerow(memory_title)
    except RuntimeError as e:
        print(e)


def callback(_type: tidevice.DataType, value: dict):
    print("R:", _type.value, value)
    if _type.value == 'cpu':
        cpu_list = list(value.values())
        try:
            with open(cpu_file, 'a+', encoding="utf-8") as df:
                csv.writer(df, lineterminator='\n').writerow(cpu_list)
        except RuntimeError as e:
            print(e)
    elif _type.value == 'fps':
        fps_list = list(value.values())
        try:
            with open(fps_file, 'a+', encoding="utf-8") as df:
                csv.writer(df, lineterminator='\n').writerow(fps_list)
        except RuntimeError as e:
            print(e)
    elif _type.value == 'memory':
        memory_list = list(value.values())
        try:
            with open(memory_file, 'a+', encoding="utf-8") as df:
                csv.writer(df, lineterminator='\n').writerow(memory_list)
        except RuntimeError as e:
            print(e)


t = tidevice.Device()
perf = tidevice.Performance(t, [tidevice.DataType.CPU, tidevice.DataType.FPS, tidevice.DataType.MEMORY,
                                ])
perf.start("com.yueyou.cyreader", callback=callback)

# time.sleep(10)
time.sleep(3600*5.5)
perf.stop()
packages = ["com.yueyou.cyreader"]
package_save_path = continue_path
report = Report(package_save_path, packages)
report.filter_file_names(package_save_path)