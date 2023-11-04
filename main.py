import api
import schedule
import time

#发送每日作业提醒
def push_unwork():
    result = api.xxt_unwork()
    match result:
        case 0:
            result_push = api.wxpusher("您没有未提交的作业","学习通作业提醒-您没有未提交的作业")
            return result_push
        case 1:
            return "登录失效，正在重新登录\n登录失败，请检查config.json学习通账号密码"
        case _:
            result_push = api.wxpusher(result,"学习通作业提醒")
            return result_push
        
#24小时内截止作业提醒
def push_unwork24():
    result = api.xxt_unwork24()
    match result:
        case 0:
            return("没有24小时内截止的作业，不做提醒")
        case 1:
            return "登录失效，正在重新登录\n登录失败，请检查config.json学习通账号密码"
        case _:
            result_push = api.wxpusher(result,"您有作业在24小时内截止，请及时完成")
            return result_push
        
def job_unwork():
    print(push_unwork())

def job_unwork24():
    print(push_unwork24())

schedule.every().day.at("21:20").do(job_unwork)
schedule.every().day.at("06:30").do(job_unwork24)
schedule.every().day.at("09:30").do(job_unwork24)
schedule.every().day.at("12:30").do(job_unwork24)
schedule.every().day.at("15:30").do(job_unwork24)
schedule.every().day.at("18:30").do(job_unwork24)
schedule.every().day.at("21:30").do(job_unwork24)
schedule.every().day.at("23:52").do(job_unwork24)

while True:
    schedule.run_pending()
    time.sleep(1)