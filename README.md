# 安装依赖并运行机器人
1. 下载 [mirai-console-loader](https://github.com/iTXTech/mirai-console-loader/releases) 并解压到当前文件夹
2. 运行 [Makefile](Makefile)：`make update run`
3. 在 mirai-console 登录机器人：`/login <qq> <password>`
4. 运行 [Makefile](Makefile)：`make bot`



# 现有功能
## 命令
以 `/` 开头的消息判定为命令，使用方法为 `/<命令名> [命令参数]`，其中全部命令的定义见 [utils/plugins](utils/plugins) 文件夹。

返回文本例子如下，于是可以发送消息 `/repeat * 3` 来调用，如果不指定参数则按照函数定义时的默认参数处理，同时参数类型也会根据 type hint 自动转化，目前不支持 `*args` 和 `**kwargs`，如果想要指定参数值可以采用 `<参数名称>~<参数值>` 调用：`/repeat number~5`。

目前内置命令 `/help [命令名]` 会自动返回函数的 docstring。

```python
from icu.decorator import commander

@commander(return_='text')  # 可简写为 @commander
def repeat(text: str = '*', number: int = 3):
    '''
    docstring
    '''
    return text * number
```

返回图片例子如下，如果想返回图片，需要在本地将图片缓存下来，函数返回本地图片的路径即可。

```python
from icu.decorator import commander

@commander(return_='image')
def heatmap(name: str = 'dust2'):
    '''
    docstring
    '''
    path = os.path.join('cache', f'{name}.png')
    assert os.path.exists(path)
    return path
```


## 关键词回复及模糊回复
关键词以二维数组的形式存储，例如 `[['你好', '再见'], ['世界']]`，第一层必须同时满足，第二层有一个满足即可，例如 "你好，世界" 与 "世界再见" 均判定为满足关键词。目前内置命令 `/add` 可以添加关键词，其中 `keyword` 为字符串类型，第一层以空格分隔，第二层以 `/` 分割。例如 `/add '你好/再见 世界' 'hello world!'` 即在关键词数据库中增加了关键词及回复 `'hello world'`。

模糊回复为根据对话找出数据库中与之类似的回复，因此关键词以字符串的形式存储即可。

```python
@commander
def add(keyword: str, return_: str):
    ...

@commander
def addfuzzy(keyword: str, return_: str):
    ...
```
