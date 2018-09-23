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
	if content[0:1]=="。":
		return chatWithMe(content[1:])
