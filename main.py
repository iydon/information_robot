# -*- coding: utf-8 -*-
# 更新插件：qq unplug QQ && qq plug QQ
from qqbot import QQBotSlot as qqbotslot, RunBot
import requests, re, random, json
# numpy, matplotlib, pandas, tensorflow
import bus



def extraFunction(contact,content,member, bot):
    # 附加功能
    if "bus" in content:
        op = re.findall("\d+", content)
        return 1,bus.bustime(int(op[0])-1 if op else None)
    return 0, ""


@qqbotslot

def onQQMessage(bot, contact, member, content):
    #if getattr(member, "uin", None) != bot.conf.qq:
    if not bot.isMe(contact, member):
        if content[0] in [";","；"] and content[-1] in [";","；"]:
            with open("data.tsv",mode="a+", encoding="utf-8") as f:
                string = content[1:-1]
                f.write(string.replace("；", "\t").replace(";", "\t")+"\n")
                return
        with open("data.tsv",encoding="utf-8") as f:
            keywords = [re.split("\t+", j) for j in re.split("[\r\n]+", f.read().strip())]
        for keyword in keywords:
            if "#" == keyword[0]:
                continue
            if len(keyword) > 1:
                or_flag = True
                for col in keyword[:-1]:
                    if "/" in col:
                        or_flag = False
                        for c in col.split("/"):
                            if c in content.lower():
                                or_flag = True
                                break
                        if not or_flag:
                            break
                    elif col.lower() not in content.lower():
                        or_flag = False
                        break
                if or_flag:
                    if keyword[-1][0]==":":
                        exec("from pluger import {0} as tmp_module".format(keyword[-1][1:]))
                        string = eval("tmp_module.onMessage(bot,contact,member,content)")
                        bot.SendTo(contact, string.replace("\\n", "\n"))
                    else:
                        bot.SendTo(contact, keyword[-1].replace("\\n", "\n"))

        flag,con = extraFunction(contact, content, member, bot)
        if flag:
            bot.SendTo(contact, con)
            return
        # shutdown
        if "sudo rm -rf /" == content or ":{:|:&};:" == content or "%0|%0" == content:
            bot.SendTo(contact, "我要休息一下~")
            bot.Stop()
            return


if __name__ == "__main__":
    RunBot()
