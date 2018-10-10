# 时间提醒
import os, time, re
from threading import Thread

def onMessage(bot, contact, member, content):
    def rem(num):
        time.sleep(num)
        bot.SendTo(contact, "%d秒已到~"%num)
    num = re.findall("\d+",content)
    num = int(num[0]) if num else 60
    t = Thread(target=rem, args=(num,))
    t.start()
    return "安排上了/亲亲"
