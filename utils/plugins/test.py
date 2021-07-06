from ..decorator import command


@command
def help(name: str = 'help'):
    '''help me
    '''
    if name in command.s:
        return command.s[name].__doc__.strip() or 'CommandHasNoDoc'
    else:
        return 'CommandNotFound'


@command
def all():
    '''get all commands
    '''
    return '\n'.join(command.s)
