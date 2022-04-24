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
# from past.builtins import raw_input
from win10toast_click import ToastNotifier


# print(res)
def date():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        'Content-Type': 'application/json',
    }
    # 注意 data中pageSize值的改变可以改变获取的商品种数
    data = {
        'typeid': '',
        'start': '0',
        'prefetype': 'undefined',
        'discount': 'undefined',
        'pageSize': '50',
        'sorttype': '',
        'sortcol': '',
        'sid': '49480',
        'spid': '49209',
        'openid': 'oz7m-4ut-JoK2RWBBa_OtzJ3aFos',
        'token': '1DF7FE5500DE1AD015E94257FCD91E7D76E387E0D5C923D59FDEFA520022182C44D31B2C5F27C5756779C0DA9EAF7637184E2095B93154D02DF74215E6134B8031A1322E63EC3C82CD07778E36B385D4B3852AFFD62E8B15D88DB2E1830B77F0B3BCAC26CC9C0E27CA3DB75A4FB5DE349BCC431C7DE76EF7E6D2014358AEE4FDFF9D3ECF25265E23883C573B8ADFB927745E0DAB46E68C21259647C745A0A7EFA8CC8D547DFCA3D35B7685AF514677182397720106B531459E79B401961B747F61F621F5D1730D6CA6B5C86172555954BD089D1F9AD48674F1A16EE0D6094390883C573B8ADFB927D180D0DD08232F1E80A27124BE050694F4A2F24BA3E420B78BE44F92E15FD5BC2FFBD385B34BA9841A985B34EC6CABF900B74D7D1B1CF539674B42BEFBDD192FCCD7794EA9E93ACCCE53E51F8B53B34FC94935CEE88031505F12D324C5B12AAA90E60E665DEEA25D181EA1487B0CA25182D0F86FFCFB77480B095DDBD1C6F6274BF0C5F6727CA6660C13C1609CFF44683195297E1BA32B487CA8D7F7CB17C05B3CAD226196AE88C9E6D5FF5C2B96E49987F1146299F697223DBED768A80237F9D9D55427E803E47579AD974E4F50F240EBA47C402B2C81F0C17FA633A7F6564F15158ACC2CBFB50FC7BFE09035B7145991AB3A6ECAA3F889CBD695D6588FAC48D573C7525A0CC2472437777EAAC6F4A50699F6AA72070FC7C8B8299B1E041D5EED5762455CCC323DBD6972E4F5E77AB81850D6E2E4F264E51D5E42C091905A749A060014FF02865B5FF4253120D7DD05F07BBC17046FDC16C64BAD6F4BAABC79731DDE8756E0460C2502301709FCF693 '
    }

    trys = 0
    while True:
        # POST请求
        Response = requests.post('https://yun.yun8609.net//wxmall/wmall/getCateInfoList', headers=headers, data=data)
        if Response.status_code == 200:  # 成功
            # trys = 0
            # print(">>"+ str(datetime.datetime.now())+",请求成功！<<")
            return Response
        else:  # 失败重试3次
            print(">>" + str(datetime.datetime.now()) + "<<" + "\n>>Error request:" + str(Response.status_code) + "<<")
            trys = trys + 1
            # if trys == 4:
            #     time.sleep(0.5)
            #     break
            time.sleep(1)
            print(">>Retry after 30s later...")
            time.sleep(30)
            print(">>>>重新请求接口...第%s次<<<<" % trys)
            time.sleep(0.5)
    # print(">>>>请求错误，请重启程序！<<<<")
    # raw_input("Press <enter>")  # 防止直接关闭窗口

    # respose = Response
    # return respose


def solve_date():
    res = date().json()
    th_name = jsonpath(res, "$..name")
    if not th_name:
        count = 0
    else:
        count = len(th_name)
    th_num = jsonpath(res, "$..stockqty")
    th_price = jsonpath(res, "$..mallmprice")
    all = []
    log_solve = 1

    # 响应中 count代表列表中商品数量 若商品列表无数据 count为0
    if count != 0:
        for i in range(0, count):
            if th_num[i] <= 0:
                th_num[i] = 0
                all.append([th_name[i], th_num[i], th_price[i]])
            else:
                all.append([th_name[i], th_num[i], th_price[i]])
    else:
        log_solve = 0

    return all, count, log_solve


# 判断商品是否是新上架或者已经下架
def judge(all, num, his_num, his_all):
    newnames = []
    hisnames = []
    for m in range(0, num):
        newnames.append(all[m][0])
    for n in range(0, his_num):
        hisnames.append(his_all[n][0])
    newgoods = set(newnames).difference(set(hisnames))
    outgoods = set(hisnames).difference(set(newnames))
    samegoods = set(hisnames).intersection(set(newnames))

    new = []
    out = []
    same = []

    if newgoods:
        for i in range(0, len(newgoods)):
            for j in range(0, num):
                if list(newgoods)[i] == all[j][0]:
                    new.append(all[j])
    if outgoods:
        for i in range(0, len(outgoods)):
            for j in range(0, his_num):
                if list(outgoods)[i] == his_all[j][0]:
                    out.append(his_all[j])
    if samegoods:
        for i in range(0, len(samegoods)):
            for j in range(0, num):
                if list(samegoods)[i] == all[j][0]:
                    same.append(all[j])
    return new, out, same


# 根据判断出来的 新上架 下架 还在 三种分别构造消息
def msg(new, out, same):
    newmsg = ""
    if new:
        for i in range(0, len(new)):
            if new[i][1] == 0:
                new[i].append("❌已售罄")
            else:
                new[i].append("✅在售中")
            newmsg = newmsg + "New!🆕\n" + ">>" + new[i][0] + "\n" + str(new[i][2]) + "元，剩余" + " [" + str(
                new[i][1]) + "]  " + new[i][3] + "\n"
    else:
        pass

    outmsg = ""
    if out:
        for i in range(0, len(out)):
            if out[i][1] == 0:
                out[i].append("❌已售罄")
            else:
                out[i].append("✅在售中")
            outmsg = outmsg + "已下架" + ">>" + out[i][0] + "[" + str(out[i][1]) + "]\n"
    else:
        pass

    samemsg = ""
    if same:
        for i in range(0, len(same)):
            if same[i][1] == 0:
                same[i].append("❌已售罄")
            else:
                same[i].append("✅在售中")
            samemsg = samemsg + ">>" + same[i][0] + "\n" + str(same[i][2]) + "元，剩余" + " [" + str(same[i][1]) + "]  " + same[i][3] + "\n"
    else:
        pass

    # if same and not new and not out:

    msgg = newmsg + outmsg + samemsg
    print(msgg)
    return msgg

    # for m in range(0,len(a)):
    #     if a[i][1] == 0:
    #         a[i].append("❌已售罄")
    #     else:
    #         a[i].append("✅在售中")
    #     newmsg = newmsg + "New\n" +str(a[i])
    # for i in range(0,len(same)):
    #     if same[i][1] == 0:
    #         same[i].append("❌已售罄")
    #     else:
    #         same[i].append("✅在售中")
    #
    #     msgg = msgg + ">>" + same[i][0] + "，" + str(all[i][2]) + "元，剩余" + " [" + str(all[i][1]) + "]  " + all[i][3] + "\n"

    # msgbox()
    # if len(his_all) != 0 and len(all) != 0:  # 旧商品列表与新商品列表都有数据
    #     if his_num == num:
    #         key = 0
    #         for i in range(0, num):
    #             if his_all[i][0] != all[i][0]:  # 若商品列表变化触发消息
    #                 key = key + 1
    #
    #                 # his_all = all
    #             elif int(his_all[i][1]) - int(all[i][1]) > 0 and all[i][1] == 0:  # 库存为0 触发消息
    #                 key = key + 1
    #                 # his_all = all
    #             elif his_all[i][1] == 0 and all[i][1] == 1 :  # 补货触发
    #                 key = key + 1
    #             else:
    #                 key = 0
    #
    #         if key != 0:
    #             msgbox1()
    #             his_all = all
    #             time.sleep(5)
    #         else:
    #             # print('商品列表未发生变化')
    #             his_all = all
    #             time.sleep(10)
    #     elif his_num != num:  # 历史与新 商品数不同 触发消息
    #         msgbox()
    #         his_all = all
    #         his_num = num
    #         time.sleep(5)
    # elif len(his_all) == 0 and len(all) != 0:  # 旧列表为空 新列表有数据 触发消息
    #     print(">>>>商店已开门！")
    #     msgbox()
    #     his_all = all
    #     time.sleep(5)
    # elif len(all) == 0 and len(his_all) != 0:  # 新商品列表为空 触发消息
    #     msgbox()
    #     his_all = all
    #     time.sleep(5)
    # elif len(his_all) == 0 and len(all) == 0:  # 新旧商品列表均为空
    #     time.sleep(10)
    #     continue


# 推送触发器
def msgTrigger(his_all, his_num, all, num, msgg):
    tozero = []
    if len(his_all) != 0 and len(all) != 0:  # 旧商品列表与新商品列表都有数据
        if his_num == num:
            for i in range(0, num):
                if his_all[i][0] != all[i][0]:  # 若商品列表变化触发消息
                    msgbox(msgg, 1, tozero)
                    # his_all = all
                elif his_all[i][1] != 0 and all[i][1] == 0:  # 库存为0 触发消息
                    tozero.append(all[i][0])
                    msgbox(msgg, 2, tozero)

                    # his_all = all
                elif all[i][1] != 0 and his_all[i][1] == 0:  # 补货触发
                    tozero.append(all[i][0])
                    msgbox(msgg, 3, tozero)


        elif his_num != num:  # 历史与新 商品数不同 触发消息
            msgbox(msgg, 1, tozero)
            # time.sleep(5)
    elif len(his_all) == 0 and len(all) != 0:  # 旧列表为空 新列表有数据 触发消息
        # print(">>>>商店已开门！")
        msgbox(msgg, 4, tozero)
        # time.sleep(5)
    elif len(all) == 0 and len(his_all) != 0:  # 新商品列表为空 触发消息
        msgbox(msgg, 5, tozero)
        # time.sleep(5)
    elif len(his_all) == 0 and len(all) == 0:  # 新旧商品列表均为空
        time.sleep(5)


# 根据触发器触发的不同task 进行消息推送
def msgbox(msgg, task, tozero):
    total = ""
    if task == 1:
        total = "\n" + msgg
    elif task == 2:
        zeromsg = ""
        for i in range(0, len(tozero)):
            zeromsg = zeromsg + tozero[i]
        total = "\n" + "以下商品售罄：⛔\n" + zeromsg + "\n商品列表：\n" + msgg
    elif task == 3:
        addmsg = ""
        for i in range(0, len(tozero)):
            addmsg = addmsg + tozero[i]
        total = "\n" + "以下商品补货：↘\n" + addmsg + "\n商品列表：\n" + msgg
    elif task == 4:
        total = "\n>>>>商店已开门！\n" + msgg
    elif task == 5:
        total = "\n商品列表为空\n" + msgg

    end = str(datetime.datetime.now()) + total
    print(end)  # 程序窗口中输出

    # pushiplus推送
    sendmessage(end)

    # 桌面通知 已知Bug: py程序封装成exe程序后，show_toast中icon无法调用报错 不影响程序运行
    toaster = ToastNotifier()
    toaster.show_toast(title="", msg=end, icon_path="default", duration=5, threaded=True)
    time.sleep(0.5)
    print("持续监控中...")


# pushplus 推送
def sendmessage(total):
    token = ''  # 需要更改你的token
    title = '商品变更通知'  # 改成你要的标题内容
    content = total  # 改成你要的正文内容
    topic = ''  # 群组编码，可以进行群发，需更改url
    url = 'http://www.pushplus.plus/send?token=' + token + '&title=' + title + '&content=' + content + '&topic=' + topic
    requests.get(url)
    time.sleep(0.5)


def main():
    his_all, his_num, his_no = solve_date()  # 先发次请求记录商品列表信息，用作后续判断触发消息通知条件
    print(">>>>正在监控商品列表.......")
    time.sleep(3)
    print("目前商品列表:")
    # msgbox()

    while True:  # 本demo使用死循环不太建议正规项目使用 建议使用schedule Task
        all, num, log_solve = solve_date()  # 获取信息 all为处理过的列表[['商品名','库存','价格'],[],...];num为商品列表中商品种类数量;
        new, out, same = judge(all, num, his_num, his_all)
        # print(new, out, same)
        msgg = msg(new, out, same)
        msgTrigger(his_all, his_num, all, num, msgg)
        his_all = all
        his_num = num
        time.sleep(5)


if __name__ == '__main__':
    # solve_date()
    # msgbox()
    main()  # 入口
