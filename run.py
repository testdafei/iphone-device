import time
import tidevice
import csv
import os
from datetime import datetime
from tools.report import Report
from configparser import ConfigParser
import re


strDate = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
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


def check_config_option(config_dic, parse, section, option):
    if parse.has_option(section, option):

        try:
            config_dic[option] = parse.get(section, option)
            if option == 'frequency':
                config_dic[option] = (int)(parse.get(section, option))
            if option == 'timeout':#timeout 的单位是分钟
                config_dic[option] = (int)(parse.get(section, option))*60
            if option in ["exceptionlog" ,"phone_log_path","space_size_check_path","package","pid_change_focus_package",
                          "watcher_users","main_activity","activity_list"]:
                if option == "activity_list" or option == "main_activity":
                    config_dic[option] = parse.get(section, option).strip().replace("\n","").split(";")
                else:
                    config_dic[option] = parse.get(section, option).split(";")
        except:#配置项中数值发生错误
            if option != 'udid':
                print("config error, please config it correctly")
            else:
                config_dic[option] = ''
    else:#配置项没有配置
        if option not in ['serialnum',"main_activity","activity_list","pid_change_focus_package","shell_file"]:
            print("config error, please config it correctly")
        else:
            config_dic[option] = ''
    return config_dic


def parse_data_from_config():
    '''
    从配置文件中解析出需要的信息，包名，时间间隔，设备的序列号等
    :return:配置文件中读出来的数值的字典
    '''
    config_dic = {}
    configpath = os.path.join(base_path, "config.conf")
    if not os.path.isfile(configpath):
        raise RuntimeError("the config file didn't exist: " + configpath)
    # 避免windows会用系统默认的gbk打开
    with open(configpath, encoding="utf-8") as f:
        content = f.read()
        # Window下用记事本打开配置文件并修改保存后，编码为UNICODE或UTF-8的文件的文件头
        # 会被相应的加上\xff\xfe（\xff\xfe）或\xef\xbb\xbf，然后再传递给ConfigParser解析的时候会出错
        # ，因此解析之前，先替换掉
        content = re.sub(r"\xfe\xff", "", content)
        content = re.sub(r"\xff\xfe", "", content)
        content = re.sub(r"\xef\xbb\xbf", "", content)
        open(configpath, 'w', encoding="utf-8").write(content)
    paser = ConfigParser()
    paser.read(configpath, encoding="utf-8")
    config_dic = check_config_option(config_dic, paser, "Common", "package")
    config_dic = check_config_option(config_dic, paser, "Common", "frequency")
    config_dic = check_config_option(config_dic, paser, "Common", "timeout")
    config_dic = check_config_option(config_dic, paser, "Common", "udid")
    config_dic = check_config_option(config_dic, paser, "Common", "save_path")

    return config_dic

config_dic = parse_data_from_config()
t = tidevice.Device(udid=config_dic['udid'])
perf = tidevice.Performance(t, [tidevice.DataType.CPU, tidevice.DataType.FPS, tidevice.DataType.MEMORY,
                                ])

perf.start(config_dic['package'][0], callback=callback)
cpu_title_writer()
fps_title_writer()
memory_title_writer()
# 运行时间:秒
time.sleep(config_dic['timeout'])
# time.sleep(60)
perf.stop()
packages = config_dic['package']
if config_dic["save_path"]:
    package_save_path = os.path.join(config_dic["save_path"], packages[0], strDate)
else:
    package_save_path = time_file
report = Report(package_save_path, packages)
report.filter_file_names(package_save_path)