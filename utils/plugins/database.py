from ..decorator import commander


def create_database_related_commands(database):
    '''
    - Argument:
        - database: Database from ..database
    '''
    @commander
    def add(keyword: str, return_: str):
        '''
        add auto-reply keywords

        - Argument:
            - keyword: str, e.g. '你好/再见 世界'
            - return_: str
        '''
        database.keyword_add(
            database.keyword_parse(keyword), return_=return_, type='text'
        )
        return 'Done'

    @commander
    def addfuzzy(keyword: str, return_: str):
        '''
        add auto-reply fuzzy keyword

        - Argument:
            - keyword: str, e.g. '你好世界'
            - return_: str
        '''
        database.keyword_add_fuzzy(keyword, return_=return_, type='text')
        return 'Done'
