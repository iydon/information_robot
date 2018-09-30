# 夜宵
import time

def onMessage(bot, contact, member, content):
	wday = time.gmtime().tm_wday+1
	if wday in [2, 5]:
		return "没有夜宵。"
	else:
		return "湖畔食堂今晚有夜宵：夜宵20:30-22:30。"
