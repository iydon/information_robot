# 讲座信息
import re, requests, time

def str2time(s):
	month  = s[:s.index("月")]
	day    = s[s.index("月")+1:s.index("日")]
	hour   = s[s.index("日")+1:s.index(":")]
	minute = s[s.index(":")+1:]
	return (int(month), int(day), int(hour), int(minute))


url = "http://sustc.edu.cn/news_events_jiangzuo/p/%d"
i = 0
d = dict()
to_time = lambda x: x[0]*86400+x[1]*3600+x[2]*60+x[3]
while True:
	i += 1
	response = requests.get(url%i)
	content  = response.content.decode("utf-8", errors="ignore")
	type_lec = re.findall("(?<=<div class=\"t0\">)[\s\S]+?(?=</div>)", content)
	titl_lec = re.findall("(?<=target=\"_self\" title=\")[\s\S]+?(?=\")", content)
	refe_lec = re.findall("(?<=<a href=\"/news_events_jiangzuo/)\d+(?=\")", content)
	urls_lec = "http://sustc.edu.cn/news_events_jiangzuo/%s"
	peop_lec = re.findall("(?<=<div class=\"t2\"><span>演讲者：</span>)[\s\S]+?(?=</div>)", content)
	time_lec = re.findall("(?<=<div class=\"t3\"><span>时间：</span>)[\s\S]+?(?=</div>)", content)
	plac_lec = re.findall("(?<=<div class=\"t4\"><span>地点：</span>)[\s\S]+?(?=</div>)", content)
	for typ,tit,peo,tim,pla,ref in zip(type_lec,titl_lec,peop_lec,time_lec,plac_lec,refe_lec):
		try:
			lec_time = str2time(tim)
		except:
			break
		struct   = time.localtime()
		now_time = (struct.tm_mon, struct.tm_mday, struct.tm_hour, struct.tm_min)
		ele_lec = to_time(lec_time)
		ele_now = to_time(now_time)
		flag    = ele_now>=ele_lec
		if flag:
			continue
		key = "%s:\n%s\n%s, %s, %s\n%s"%(typ, tit, peo, tim, pla, urls_lec%ref)
		d[key] = lec_time
	if flag:
		break

d_sorted = sorted(d, key=lambda x:to_time(d[x]))

def onMessage(bot, contact, member, content):
	dig = re.findall("\d+", content)
	if dig:
		dig = int(dig[0])
	else:
		dig = 5
	for msg in d_sorted[:dig]:
		bot.SendTo(contact, msg)
		time.sleep(0.1)
	return "Done"

