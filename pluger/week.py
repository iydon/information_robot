# 周次
import time

def onMessage(bot, contact, member, content):
	week = (time.gmtime().tm_yday-1)//7 - 34
	week -= 1 if week>5 else 0
	return "本周是第%d周~"%week

