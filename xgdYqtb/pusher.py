import requests, os

def pusher(*args):
    testmsg = ""
    msg = args[0]
    othermsg = ""
    for i in range(1, len(args)):
        othermsg += args[i]
        othermsg += "\n"
    SCKEY = os.environ.get('SCKEY') # http://sc.ftqq.com/
    SCTKEY = os.environ.get('SCTKEY') # http://sct.ftqq.com/
    Skey = os.environ.get('Skey') # https://cp.xuthus.cc/
    Smode = os.environ.get('Smode') # send, group, psend, pgroup, wx, tg, ww, ding(no send email)
    pushplus_token = os.environ.get('pushplus_token') # http://www.pushplus.plus/
    pushplus_topic = os.environ.get('pushplus_topic') # pushplus一对多推送需要的"群组编码"，一对一推送不用管
    tg_token = os.environ.get('tg_token') # telegram bot的Token，telegram机器人通知推送必填项
    tg_chatid = os.environ.get('tg_chatid') #接收通知消息的telegram用户的id，telegram机器人通知推送必填项
    tg_api_host = os.environ.get('tg_api_host') # Telegram api自建的反向代理地址(不懂忽略)，默认tg官方api=api.telegram.org
    if SCKEY:
        sendurl = f"https://sc.ftqq.com/{SCKEY}.send"
        data = {
            "text" : msg,
            "desp" : othermsg
            }
        r = requests.post(sendurl, data=data)
        testmsg += f"{r.text}\n"
    if SCTKEY:
        sendurl = f"https://sctapi.ftqq.com/{SCTKEY}.send"
        data = {
            "title" : msg,
            "desp" : othermsg
            }
        r = requests.post(sendurl, data=data)
        testmsg += f"{r.text}\n"
    if pushplus_token:
        sendurl = "http://www.pushplus.plus/send"
        if not othermsg:
            othermsg = msg
        if pushplus_topic:
            params = {
                "token" : pushplus_token,
                "title" : msg,
                "content" : othermsg,
                "template" : "html",
                "topic" : pushplus_topic
            }
        else:
            params = {
                "token" : pushplus_token,
                "title" : msg,
                "content" : othermsg,
                "template" : "html"
            }
        r = requests.post(sendurl, params=params)
        testmsg += f"{r.text}\n"
        if r.json()["code"] != 200:
            print(r.json())
            print(f"pushplus推送失败！{r.json()['msg']}")
    if Skey:
        if not Smode:
            Smode = 'send'
        if othermsg:
            msg = msg + "\n" + othermsg
        sendurl = f"https://push.xuthus.cc/{Smode}/{Skey}"
        params = {"c" : msg}
        r = requests.post(sendurl, params=params)
        testmsg += f"{r.text}\n"
    if tg_token and tg_chatid:
        if tg_api_host:
            sendurl = f'https://{tg_api_host}/bot{tg_token}/sendMessage'
        else:
            sendurl = f'https://api.telegram.org/bot{tg_token}/sendMessage'
        params = {
            "chat_id" : tg_chatid,
            "text" : f'{msg}\n{othermsg}'
            }
        r = requests.post(sendurl, data=params)
        testmsg += f"{r.text}\n"
    return testmsg


