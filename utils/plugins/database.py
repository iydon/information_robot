from ..decorator import commander


def create_database_related_commands(database):
    '''
    Argument:
        - database: Database from ..database
    '''
    @commander
    def add(keyword: str, return_: str):
        '''add auto-reply keywords

        Argument:
            - keyword: str, e.g. '你好/再见 世界'
            - return_: str
        '''
        database.keyword_add(
            database.keyword_parse(keyword),
            return_=return_, type='text',
        )
        return 'Done'
