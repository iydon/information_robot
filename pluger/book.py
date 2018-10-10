# 书籍推荐
import random, re, requests

def crawl(url):
    res = requests.get(url)
    intro = re.findall("(?<=<div class=\"intro\">)[\s\S]+?(?=</div>)", res.text)
    return ["\n".join(re.findall("(?<=<p>)[\s\S]+?(?=</p>)", i)) for i in intro]

def onMessage(bot, contact, member, content):
    with open("pluger/Book", mode="r", encoding="utf-8") as f:
        d = eval(f.read())
    idx = len(d['题目'])
    idx = random.randint(0, idx-1)
    string = "《%s》\n%s\n"%(d['题目'][idx],d['出版'][idx])
    string += "%s: %s\n%s"%(d['人数'][idx],d['等级'][idx],d['链接'][idx])
    intro = crawl(d['链接'][idx])
    bot.SendTo(contact, string)
    bot.SendTo(contact, "作品:\n%s"%intro[0])
    bot.SendTo(contact, "作者:\n%s"%intro[-1])
    return "以上"
