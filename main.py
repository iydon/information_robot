# -*- coding: utf-8 -*-
# 更新插件：qq unplug QQ && qq plug QQ
from qqbot import QQBotSlot as qqbotslot, RunBot
import requests, re, random, json
# numpy, matplotlib, pandas, tensorflow
import bus



def extraFunction(contact,content,member, bot):
    # 附加功能
    if content=='bus':
        return 1,bus.bustime()
    return 0, ""


@qqbotslot

def onQQMessage(bot, contact, member, content):
    #if getattr(member, 'uin', None) != bot.conf.qq:
    if not bot.isMe(contact, member):
        if contact.name: # in ['南科大信息交流群','智商404','信交群qqbot编写小组']:
            if content[0] in [';','；'] and content[-1] in [';','；']:
                with open('data.tsv',mode='a+', encoding='utf-8') as f:
                    string = content[1:-1]
                    f.write(string.replace('；', '\t').replace(';', '\t')+'\n')
                    return
            with open('data.tsv',encoding='utf-8') as f:
                keywords = [re.split('\t+', j) for j in re.split('[\r\n]+', f.read().strip())]
            for keyword in keywords:
                if '#' in str(keyword):
                    continue
                if len(keyword)==2:
                    if keyword[0].lower() in content.lower():
                        bot.SendTo(contact, keyword[-1])
                elif len(keyword)>2:
                    if keyword[0]:
                        tmp = keyword[0]
                    else:
                        keyword[0] = tmp
                    or_flag = True
                    for col in keyword[:-1]:
                        if col.lower() not in content.lower():
                            or_flag = False
                            break
                    if or_flag:
                        if keyword[-1][0]==':':
                            string = __import__(keyword[-1][1:]).onMessage(bot, contact, member, content)
                            bot.SendTo(contact, string)
                        else:
                            bot.SendTo(contact, keyword[-1])
            
            flag,con = extraFunction(contact, content, member, bot)
            if flag:
                bot.SendTo(contact, con)
                return
            # shutdown
            if contact.name=='智商404':
                if 'rm -rf /' == content or ':{:|:&};:' == content or '%0|%0' == content:
                    bot.SendTo(contact, '我要休息一下~')
                    bot.Stop()
                    return


if __name__ == '__main__':
    RunBot()
