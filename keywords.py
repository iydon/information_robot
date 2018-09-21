def onMessage(bot, contact, member, content):
	string = ""
	with open("data.tsv") as f:
		lines = f.read().split("\n")
		for line in lines:
			string += ",".join(line.split("\t")[:-1]) + ";"
	return string[:-1]
