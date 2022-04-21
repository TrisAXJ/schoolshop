# !/usr/bin/python3.10
# -*- coding: utf-8 -*-
# Author:_TRISA_
# File:sss.py
# Time:2022/4/19 22:08
# Software:PyCharm
# Email:1628791325@QQ.com
# -U2hhcmUlMjBhbmQlMjBMb3Zl-base64

import datetime
import requests
import time
from jsonpath import jsonpath
from past.builtins import raw_input
from win10toast_click import ToastNotifier


# print(res)
def date():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        'Content-Type': 'application/json',
    }

    data = {
        'typeid': '',
        'start': '0',
        'prefetype': 'undefined',
        'discount': 'undefined',
        'pageSize': '10',
        'sorttype': '',
        'sortcol': '',
        'sid': '49480',
        'spid': '49209',
        'openid': 'oz7m-4ut-JoK2RWBBa_OtzJ3aFos',
        'token': '1DF7FE5500DE1AD015E94257FCD91E7D76E387E0D5C923D59FDEFA520022182C44D31B2C5F27C5756779C0DA9EAF7637184E2095B93154D02DF74215E6134B8031A1322E63EC3C82CD07778E36B385D4B3852AFFD62E8B15D88DB2E1830B77F0B3BCAC26CC9C0E27CA3DB75A4FB5DE349BCC431C7DE76EF7E6D2014358AEE4FDFF9D3ECF25265E23883C573B8ADFB927745E0DAB46E68C21259647C745A0A7EFA8CC8D547DFCA3D35B7685AF514677182397720106B531459E79B401961B747F61F621F5D1730D6CA6B5C86172555954BD089D1F9AD48674F1A16EE0D6094390883C573B8ADFB927D180D0DD08232F1E80A27124BE050694F4A2F24BA3E420B78BE44F92E15FD5BC2FFBD385B34BA9841A985B34EC6CABF900B74D7D1B1CF539674B42BEFBDD192FCCD7794EA9E93ACCCE53E51F8B53B34FC94935CEE88031505F12D324C5B12AAA90E60E665DEEA25D181EA1487B0CA25182D0F86FFCFB77480B095DDBD1C6F6274BF0C5F6727CA6660C13C1609CFF44683195297E1BA32B487CA8D7F7CB17C05B3CAD226196AE88C9E6D5FF5C2B96E49987F1146299F697223DBED768A80237F9D9D55427E803E47579AD974E4F50F240EBA47C402B2C81F0C17FA633A7F6564F15158ACC2CBFB50FC7BFE09035B7145991AB3A6ECAA3F889CBD695D6588FAC48D573C7525A0CC2472437777EAAC6F4A50699F6AA72070FC7C8B8299B1E041D5EED5762455CCC323DBD6972E4F5E77AB81850D6E2E4F264E51D5E42C091905A749A060014FF02865B5FF4253120D7DD05F07BBC17046FDC16C64BAD6F4BAABC79731DDE8756E0460C2502301709FCF693 '
    }

    trys = 0
    while trys <= 3:
        Response = requests.post('https://yun.yun8609.net//wxmall/wmall/getCateInfoList', headers=headers, data=data)
        if Response.status_code == 200:
            trys = 0
            return Response
        else:
            print("Error request:" + str(Response.status_code))
            trys = trys + 1
            print("Retry after 5s later...")
            time.sleep(5)
            print("请求接口...第%s次" % trys)
            if trys == 4:
                print("请求错误，请重启程序！")
                raw_input("Press <enter>")

    # respose = Response
    # return respose


def solve_date():
    res = date().json()
    count = jsonpath(res, "$..count")
    th_name = jsonpath(res, "$..name")
    th_num = jsonpath(res, "$..stockqty")
    th_price = jsonpath(res, "$..mallmprice")
    all = []
    log_solve = 1

    if count:
        for i in range(0, count[0]):
            if th_num[i] <= 0:
                th_num[i] = 0
                all.append([th_name[i], th_num[i], th_price[i]])
            else:
                all.append([th_name[i], th_num[i], th_price[i]])
    else:
        log_solve = 0

    return all, count, log_solve


def msgbox():
    all, num, log_solve = solve_date()
    msg = all
    msgg = ""
    if log_solve == 1:
        for i in range(0, num[0]):
            if msg[i][1] == 0:
                msg[i].append("❌已售罄")
            else:
                msg[i].append("✅在售中")

            msgg = msgg + msg[i][0] + str(msg[i][2]) + "元,剩余" + " [" + str(msg[i][1]) + "]  " + msg[i][3] + "\n"
    else:
        msgg = "商店商品列表为空"

    total = str(datetime.datetime.now()) + "\n" + msgg
    print(total)

    toaster = ToastNotifier()
    toaster.show_toast(title="", msg=total, icon_path="default", duration=5, threaded=True)
    time.sleep(0.5)
    print("持续监控中...")


def main():
    his_all, his_num, his_no = solve_date()
    print("接口监控中...")
    time.sleep(3)
    while True:
        all, num, log_solve = solve_date()
        # msgbox()
        if his_all and all:  # 判断历史商品列表与新商品列表是否都有数据
            for i in range(0, num[0]):
                if his_num == num:
                    if his_all[i][0] != all[i][0]:  # 若商品列表变化触发消息
                        msgbox()
                        his_all = all
                        time.sleep(5)
                    elif int(his_all[i][1]) - int(all[i][1]) > 0 and all[i][1] == 0: # 库存为0 触发消息
                        msgbox()
                        his_all = all
                        time.sleep(5)
                elif his_num != num: # 历史与新 商品数不同 触发消息
                    msgbox()
                    his_all = all
                    time.sleep(5)
        elif all == False and his_all: # 新列表为空 触发消息
            msgbox()
            his_all = all
            time.sleep(5)
        elif his_all == False and all:
            print(">>>>商店已开门！")
            msgbox()
            time.sleep(5)
        elif his_all ==False and all == False:
            continue


if __name__ == '__main__':
    # solve_date()
    # msgbox()
    main()
