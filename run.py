import time
import tidevice
import csv
import os,sys
import datetime

import os
from datetime import datetime

from tools.excel import Excel
from tools.report import Report
strDate = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

t = tidevice.Device()
perf = tidevice.Performance(t, [tidevice.DataType.CPU, tidevice.DataType.FPS, tidevice.DataType.MEMORY,
                                tidevice.DataType.NETWORK, tidevice.DataType.PAGE])
# perf = tidevice.Performance(t)
# strDate = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
base_path = os.path.dirname(os.path.abspath(__file__))
time_file = os.path.join(base_path, 'results', 'com.yueyou.cyreader', strDate)
os.makedirs(time_file)
cpu_file = os.path.join(time_file, 'cpuinfo.csv')
fps_file = os.path.join(time_file, 'fpsinfo.csv')
memory_file = os.path.join(time_file, 'memoryinfo.csv')


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


perf.start("com.yueyou.cyreader", callback=callback)
cpu_title_writer()
fps_title_writer()
memory_title_writer()
# time.sleep(10)
time.sleep(3600*8)
perf.stop()
packages = ["com.yueyou.cyreader"]
package_save_path = time_file
report = Report(package_save_path, packages)
report.filter_file_names(package_save_path)