import base64
import json
import subprocess
import textwrap

from icu.decorator import command, commander


def register_common_commands():
    @commander(public=True)
    def help(name: str = 'help'):
        '''
        获取命令 `name` 的帮助信息

        - 参数:
            - name，字符串，默认为 'help'

        - 例子：
            - /help add
        '''
        if name in command.s:
            doc = command.s[name]['_'].__doc__
            return textwrap.dedent(doc).strip() if isinstance(doc, str) \
                else 'CommandHasNoDoc'
        else:
            return 'CommandNotFound'

    @commander(public=True)
    def all():
        '''
        获取所有公开的命令
        '''
        return ', '.join(k for k, v in command.s.items() if v.get('public', True))

    @commander(public=False)
    def cmd(statement: str = 'ZWNobyBoZWxsbyB3b3JsZA=='):
        '''
        运行指令

        - 参数:
            - statement，字符串，默认为 'ZWNobyBoZWxsbyB3b3JsZA=='
        '''
        command = base64.b64decode(statement).decode()
        pipe = subprocess.PIPE
        proc = subprocess.run(command, shell=True, stdout=pipe, stderr=pipe)
        result = {
            'o': proc.stdout.decode(errors='replace'),  # stdout
            'e': proc.stderr.decode(errors='replace'),  # stderr
        }
        return base64.b85encode(json.dumps(result).encode()).decode()


def register_database_commands(database):
    '''
    - Argument:
        - database: Database from icu.database
    '''
    @commander(public=True)
    def add(keyword: str, return_: str):
        '''
        添加自动回复关键词

        - 参数:
            - keyword：字符串，例如 '你好/再见 世界'
                - 格式：空格分隔为满足全部，斜线分隔为满足其一
            - return_：字符串，例如 'hello world'

        - 例子：
            - /add '你好/再见 世界' 'hello world'
        '''
        database.keyword_add(
            database.keyword_parse(keyword), return_=return_, type='text'
        )
        return 'Done'

    @commander(public=True)
    def addfuzzy(keyword: str, return_: str):
        '''
        自动添加模糊匹配关键词

        - 参数:
            - keyword：字符串，例如 '你好世界'
            - return_：字符串，例如 'hello world'

        - 例子：
            - /addfuzzy '你好世界' 'hello world'
        '''
        database.keyword_add_fuzzy(keyword, return_=return_, type='text')
        return 'Done'
