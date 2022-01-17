# 西工大疫情填报github action版本

**自动打卡仅用于学习目的，任何与疫情相关的情况请如实填写！**

程序会复用你上次填报的结果，所以需要保证自己曾经填报过

---

## 腾讯云SCF使用（推荐）

1. 从github获取release版本zip包
2. 在SCF中[新建函数](0001.jpg)

## github action使用

1. 点击项目右上角的Fork，Fork此项目
2. 到自己Fork的项目点击Actions，如果未启用，需要手动启用，然后启用需要运行的Workflows
3. 到自己Fork的项目点击Setting→Secrets→New secrets
4. 填写Name和Value
5. 在"Actions"中的"run"下点击"Run workflow"即可手动执行签到，后续运行按照schedule，默认在每天9:00自动签到，可自行修改
6. 有问题可以提issue

## 几个环境变量

| 说明  | Key          |
| ----- | ------------ |
| *学号 | xgd_username |
| *密码 | xgd_password |
| 推送  | 可选         |

## 推送可以设置的参数

> Key(名称) --> Value(值) 

Github Actions添加在Setting→Secrets→New secrets，腾讯云函数SCF设置在环境变量里

1. Key: SCKEY --> Value: [Server酱的推送SCKEY的值](http://sc.ftqq.com/)
2. Key: SCTKEY --> Value: [Server酱·Turbo版的推送SCTKEY的值](http://sct.ftqq.com/)
3. Key: Skey --> Value: [酷推调用代码Skey](https://cp.xuthus.cc/)
4. Key: Smode --> Value: 酷推的推送渠道，不设置默认send.可选参数(send,group,psend,pgroup,wx,tg,ww,ding)
5. Key: pushplus_token --> Value: [pushplus推送token](http://www.pushplus.plus/)
6. Key: pushplus_topic --> Value: pushplus一对多推送需要的"群组编码"，一对一推送不用管填了报错
7. Key: tg_token --> Value: Telegram bot的Token，Telegram机器人通知推送必填项
8. Key: tg_chatid --> Value: 接收通知消息的Telegram用户的id，Telegram机器人通知推送必填项
9. Key: tg_api_host --> Value: Telegram api自建的反向代理地址(不懂忽略此项)，默认tg官方api=api.telegram.org

