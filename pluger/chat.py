# 闲聊
import requests

def chatWithMe(content):
    api = 'http://www.tuling123.com/openapi/api?key=e715661ec2c541d7aeab0a14ae100370&info='
    dct = eval(requests.get(api+content).text)
    text = dct['text']
    if 'url' in dct.keys():
        text += ' %s'%dct['url']
    if 'list' in dct.keys():
        text += '\n%s'%(', '.join(dct['list'][randint(0,len(dct['list'])-1)].values()))
    return text

def onMessage(bot, contact, member, content):
    with open("rec.inf", mode="a+", encoding="utf-8") as f:
        f.write("%s\t%s\t%s\n"%(contact.name, member, content.replace("\n", "\\n")))
    return chatWithMe(content)
