import typing

from fuzzywuzzy import process
from tinydb import TinyDB

from .plugins.database import create_database_related_commands


class Database:
    def __init__(self, path):
        db = TinyDB(path, ensure_ascii=False, encoding='utf-8')
        self.table = {
            'keyword': db.table('keyword'),
        }
        self.cache = self._cache()
        create_database_related_commands(self)

    def keyword_add(self, keyword, return_, type='text', update=True):
        '''
        add keyword

        - Argument:
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
            self.cache = self._cache()

    def keyword_add_fuzzy(self, keyword, return_, type='text', update=True):
        '''
        add fuzzy keyword

        - Argument:
            - keyword: str
            - return_: JSON serializable
            - type: str, default 'text'
            - update: bool, default True
        '''
        assert isinstance(keyword, str) and isinstance(type, str)
        self.table['keyword'].insert(
            {'keyword': keyword, 'return': return_, 'type': type}
        )
        if update:
            self.cache = self._cache()

    def keyword_match(self, string, fuzzy=0):
        '''
        match keyword to get returns

       -  Argument:
            - string: str
            - fuzzy: int, default 0, fuzzy search limit

        - Return:
            - Iterator[JSON serializable]
        '''
        string = string.lower()
        if fuzzy:
            for key, _ in process.extractBests(
                string, self.cache['fuzzy'].keys(), limit=fuzzy
            ):
                yield self.cache['fuzzy'][key]
        else:
            for item in self.cache['keyword']:
                if not isinstance(item['keyword'], str) and all(
                    any(k2 in string for k2 in k1) for k1 in item['keyword']
                ):
                    yield {'return': item['return'], 'type': item['type']}

    def keyword_parse(self, keyword):
        '''
        parase keyword from str

        - Argument:
            - keyword: str

        - Example:
            >>> self.keyword_parse('你好/再见 世界')
            [['你好', '再见'], ['世界']]
        '''
        return list(k.split('/') for k in keyword.split())

    def _cache(self):
        cache = {'keyword': self.table['keyword'].all(), 'fuzzy': dict()}
        for item in cache['keyword']:
            if isinstance(item['keyword'], str):
                return_ = item['keyword'] + ' -> ' + item['return']
                cache['fuzzy'][item['keyword']] = {
                    'return': return_, 'type': item['type']
                }
            # else:  # List[List[str]]
            #     keyword = ''.join(map(''.join, item['keyword']))
            #     cache['fuzzy'][keyword] = {
            #         'return': item['return'], 'type': item['type']
            #     }
        return cache


if __name__ == '__main__':
    d = Database('db.json')
    d.keyword_add(
        d.keyword_parse('你好/再见 世界'),
        return_='hello world', type='text',
    )
    for item in d.keyword_match('你好，世界！'):
        print(item)
