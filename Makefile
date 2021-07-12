JAVA = java
PYTHON = python3
MCL = $(JAVA) -jar mcl.jar
POETRY = $(PYTHON) -m poetry run python


.PHNOY: run
run:
	$(MCL) --disable-update

.PHNOY: update
update:
	$(MCL) --update-package net.mamoe:mirai-console --version 2.5.0
	$(MCL) --update-package net.mamoe:mirai-login-solver-selenium --channel nightly --type plugin
	$(MCL) --update-package net.mamoe:mirai-api-http --channel stable --type plugin

.PHNOY: bot
bot:
	$(POETRY) main.py

.PHNOY: scp
scp:
	scp -r ../$(notdir $(CURDIR)) bot@bot.iydon.top:~/Desktop
