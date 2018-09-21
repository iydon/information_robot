import time

def onMessage(bot, contact, member, content):
	wday = time.gmtime().tm_wday+1
	dct = {
		1: "06:30-08:30\n18:30-21:30",
		2: "06:30-08:30\n18:30-21:30",
		3: "18:30-21:30",
		4: "18:30-21:30",
		5: "06:30-08:30\n18:30-21:30",
		6: "06:30-08:30\n15:00-17:00\n18:30-21:30",
		7: "闭馆（清洗、消毒）"
	}
	return "今日游泳馆开放时间：\n%s"%dct[wday]
