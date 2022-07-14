# encoding: utf-8
'''
@author:     look

@copyright:  1999-2020 Alibaba.com. All rights reserved.

@license:    Apache Software License 2.0

@contact:    390125133@qq.com
'''
import os
from datetime import datetime

from tools.excel import Excel
strDate = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
class Report(object):
    def __init__(self, csv_dir, packages=[]):
        os.chdir(csv_dir)
        # 需要画曲线的csv文件名
        self.summary_csf_file={"cpuinfo.csv":{"table_name":"pid_cpu",
                                          "x_axis":"timestamp",
                                          "y_axis":"%",
                                          "values":["device_cpu_rate","system_cpu_rate"]},
                               "memoryinfo.csv":{"table_name":"pid_pss",
                                          "x_axis":"timestamp",
                                          "y_axis":"mem(MB)",
                                          "values":["value","total_pss(MB)"]},
                               "fpsinfo.csv": {"table_name": "fps",
                                           "x_axis": "timestamp",
                                           "y_axis": "fps",
                                           "values": ["value"]},
                               }
        self.packages = packages
        # if len(self.packages)>0:
        #     for package in self.packages:
        #         pss_detail_dic ={"table_name":"pss_detail",
        #                                   "x_axis":"datatime",
        #                                   "y_axis":"mem(MB)",
        #                                   "values":["pss","java_heap","native_heap","system"]
        #         }
        #         #        文件名太长会导致写excel失败
        #         self.summary_csf_file["pss_%s.csv"%package.split(".")[-1].replace(":","_")]= pss_detail_dic
        file_names = self.filter_file_names(csv_dir)
        if file_names:
            book_name = 'summary_ios_%s.xlsx' % strDate
            excel = Excel(book_name)
            for file_name in file_names:
                values = self.summary_csf_file[file_name]
                excel.csv_to_xlsx(file_name,values["table_name"],values["x_axis"],values["y_axis"],values["values"])
            excel.save()
    #
    def filter_file_names(self, device):
        csv_files = []
        for f in os.listdir(device):
            if os.path.isfile(os.path.join(device, f)) and os.path.basename(f) in self.summary_csf_file.keys():
               csv_files.append(f)
        return csv_files
        #return [f for f in os.listdir(device) if os.path.isfile(os.path.join(device, f)) and os.path.basename(f) in self.summary_csf_file.keys()]

if __name__ == '__main__':
# 根据csv生成excel汇总文件
#     from mobileperf.android.globaldata import RuntimeData
    packages = ["com.yueyou.cyreader"]
    package_save_path = "/Users/admin/PycharmProjects/taobao-iphone-device/results/com.yueyou.cyreader/2022_07_12_19_40_14"
    report = Report(package_save_path,packages)
    report.filter_file_names(package_save_path)
