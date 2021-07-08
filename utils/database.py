import typing

from tinydb import TinyDB

from .plugins.database import create_database_related_commands


class Database:
    def __init__(self, path):
        db = TinyDB(path, ensure_ascii=False, encoding='utf-8')
        self.table = {
            'keyword': db.table('keyword'),
        }
        self.cache = {
            'keyword': self.table['keyword'].all(),
        }
        create_database_related_commands(self)

    def keyword_add(self, keyword, return_, type='text', update=True):
        '''add keyword

        Argument:
            - keyword: List[List[str]]
            - return_: JSON serializable
            - type: str, default 'text'
            - update: bool, default True
        '''
        assert isinstance(keyword, typing.Iterable) and all(
            isinstance(k1, typing.Iterable) and all(
                isinstance(k2, str) for k2 in k1
            ) for k1 in keyword
        ) and isinstance(type, str)
        keyword = list(list(map(str.lower, k)) for k in keyword)
        self.table['keyword'].insert(
            {'keyword': keyword, 'return': return_, 'type': type}
        )
        if update:
            self.cache['keyword'] = self.table['keyword'].all()

    def keyword_match(self, string):
        '''match keyword to get returns

        Argument:
            - string: str

        Return:
            - Iterator[JSON serializable]
        '''
        string = string.lower()
        for item in self.cache['keyword']:
            if all(
                any(k2 in string for k2 in k1) for k1 in item['keyword']
            ):
                yield {'return': item['return'], 'type': item['type']}

    def keyword_parse(self, keyword):
        '''parase keyword from str

        Argument:
            - keyword: str

        Example:
            >>> self.keyword_parse('你好/再见 世界')
            [['你好', '再见'], ['世界']]
        '''
        return list(k.split('/') for k in keyword.split())


if __name__ == '__main__':
    d = Database('db.json')
    d.keyword_add(
        d.keyword_parse('你好/再见 世界'),
        return_='hello world', type='text',
    )
    for item in d.keyword_match('你好，世界！'):
        print(item)
