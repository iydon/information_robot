# 关键词
import re

def onMessage(bot, contact, member, content):
    string = ""
    with open("data.tsv", mode="r", encoding="utf-8") as f:
        lines = f.read().split("\n")
        for line in lines:
            if "以下资料不从关键词中出现" in line:
                break
            if "#" in line:
                continue
            string += " ".join(re.split("\t+", line)[:-1]) + ";"
    return string[:-1]
