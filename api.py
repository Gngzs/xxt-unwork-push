import requests
import json
from bs4 import BeautifulSoup
import re


def xxt_login():
    # 读取配置文件
    with open("config.json", "r") as jsonfile:
        config = json.load(jsonfile)
    uname = config["xxt"]["uname"]
    password = config["xxt"]["password"]
    # 请求学习通登录api
    header = {"Accept": "application/json, text/javascript, */*; q=0.01",
              "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    data = {"fid": "-1", "uname": uname, "password": password,
            "refer": "http%3A%2F%2Fi.mooc.chaoxing.com"}
    result = requests.post(
        "https://passport2.chaoxing.com/fanyalogin", data=data, headers=header)
    results = json.loads(result.text)
    # 判断是否登录成功
    if results["status"]:
        # 获取cookie
        cookies = result.cookies.items()
        cookie = ""
        for name, value in cookies:
            cookie += '{0}={1};'.format(name, value)
        # 保存cookie
        config["xxt"]["cookie"] = cookie
        with open("config.json", "w") as jsonfile:
            json.dump(config, jsonfile, ensure_ascii=False)
        return True
    else:
        return False


def xxt_work():
    with open("config.json", "r") as jsonfile:
        config = json.load(jsonfile)
    cookie = config["xxt"]["cookie"]
    headers = {"Cookie": cookie,
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36', 'Host': 'mooc1-api.chaoxing.com'}
    result = requests.get(
        "https://mooc1-api.chaoxing.com/work/stu-work", headers=headers)
    return result.text


def xxt_unwork():
    html_doc = xxt_work()
    soup = BeautifulSoup(html_doc, "html.parser")
    title = soup.title.text
    if title != "作业列表":
        login = xxt_login()
        if login:
            html_doc = xxt_work()
            soup = BeautifulSoup(html_doc, "html.parser")
            unfinished_soups = soup.find_all(
                attrs={"aria-label": re.compile("作业名称(.*?)作业状态未提交(.*?)")})
            if unfinished_soups != -1:
                res = list(map(str, unfinished_soups))
                unfinished_list = []
                for unfinished_soup in res:
                    work_name = unfinished_soup[unfinished_soup.find(
                        "作业名称")+4:unfinished_soup.find("作业状态")]
                    work_statu = unfinished_soup[unfinished_soup.find(
                        "作业状态")+4:unfinished_soup.find("所属课程")]
                    if unfinished_soup.find("剩余时间剩余") != -1:
                        work_time = unfinished_soup[unfinished_soup.find(
                            "时间剩余")+4:unfinished_soup.find("\"></span>")]
                    else:
                        work_time = "未设置截止时间，请尽快完成"
                    unfinished_list.append(
                        "作业名称："+work_name+"\n作业状态："+work_statu+"\n剩余时间："+work_time+"\n")
                return "\n".join(unfinished_list)
            else:
                return 0
        else:
            return 1 #登录失效，正在重新登录\n登录失败，请检查学习通账号密码
    else:
        soup = BeautifulSoup(html_doc, "html.parser")
        unfinished_soups = soup.find_all(
            attrs={"aria-label": re.compile("作业名称(.*?)作业状态未提交(.*?)")})
        if unfinished_soups != -1:
            res = list(map(str, unfinished_soups))
            unfinished_list = []
            for unfinished_soup in res:
                work_name = unfinished_soup[unfinished_soup.find(
                    "作业名称")+4:unfinished_soup.find("作业状态")]
                work_statu = unfinished_soup[unfinished_soup.find(
                    "作业状态")+4:unfinished_soup.find("所属课程")]
                if unfinished_soup.find("剩余时间剩余") != -1:
                    work_time = unfinished_soup[unfinished_soup.find(
                        "时间剩余")+4:unfinished_soup.find("\"></span>")]
                else:
                    work_time = "未设置截止时间，请尽快完成"
                unfinished_list.append(
                    "作业名称："+work_name+"\n作业状态："+work_statu+"\n剩余时间："+work_time+"\n")
            return "\n".join(unfinished_list)
        else:
            return 0


def xxt_unwork24():
    html_doc = xxt_work()
    soup = BeautifulSoup(html_doc, "html.parser")
    title = soup.title.text
    if title != "作业列表":
        login = xxt_login()
        if login:
            html_doc = xxt_work()
            soup = BeautifulSoup(html_doc, "html.parser")
            unfinished_soups = soup.find_all(
                attrs={"aria-label": re.compile("作业名称(.*?)作业状态未提交(.*?)")})
            if unfinished_soups != -1:
                res = list(map(str, unfinished_soups))
                unfinished_list = []
                for unfinished_soup in res:
                    if unfinished_soup.find("剩余时间剩余") != -1:
                        work_time24 = unfinished_soup[unfinished_soup.find(
                            "时间剩余")+4:unfinished_soup.find("小时")]
                        if int(work_time24) < 24:
                            work_name = unfinished_soup[unfinished_soup.find(
                                "作业名称")+4:unfinished_soup.find("作业状态")]
                            work_time = unfinished_soup[unfinished_soup.find(
                                "时间剩余")+4:unfinished_soup.find("\"></span>")]
                            unfinished_list.append(
                                "作业名称："+work_name+"\n剩余时间："+work_time+"\n")
                if unfinished_list != []:
                    return "以下作业将在24小时内截止，请尽快完成！"+"\n".join(unfinished_list)
                else:
                    return 0
            else:
                return 0
        else:
            return 1
    else:
        soup = BeautifulSoup(html_doc, "html.parser")
        unfinished_soups = soup.find_all(
            attrs={"aria-label": re.compile("作业名称(.*?)作业状态未提交(.*?)")})
        if unfinished_soups != -1:
            res = list(map(str, unfinished_soups))
            unfinished_list = []
            for unfinished_soup in res:
                if unfinished_soup.find("剩余时间剩余") != -1:
                    work_time24 = unfinished_soup[unfinished_soup.find(
                        "时间剩余")+4:unfinished_soup.find("小时")]
                    if int(work_time24) < 24:
                        work_name = unfinished_soup[unfinished_soup.find(
                            "作业名称")+4:unfinished_soup.find("作业状态")]
                        work_time = unfinished_soup[unfinished_soup.find(
                            "时间剩余")+4:unfinished_soup.find("\"></span>")]
                        unfinished_list.append(
                            "作业名称："+work_name+"\n剩余时间："+work_time+"\n")
            if unfinished_list != []:
                return "以下作业将在24小时内截止，请尽快完成！"+"\n".join(unfinished_list)
            else:
                return 0
        else:
            return 0


def wxpusher(content, summary):
    with open("config.json","r") as jsonfile:
        config_push = json.load(jsonfile)
    appToken = config_push["wxpusher"]["token"]
    uids = config_push["wxpusher"]["uid"]
    headers = {"Content-Type":"application/json"}
    data = {
        "appToken": appToken,
        "content": content,
        "summary": summary,
        "contentType": 1,
        "uids": [
            uids
        ],
        "verifyPay": False
    }
    result = requests.post("https://wxpusher.zjiecode.com/api/send/message",headers=headers,data=json.dumps(data))
    results = json.loads(result.text)
    return results["msg"]


print(wxpusher(xxt_unwork(),"学习通作业提醒"))
