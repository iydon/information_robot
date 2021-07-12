import os

from .why import why as _why
from ..decorator import command, commander


@commander
def help(name: str = 'help'):
    '''get the docstring of the command `name`

    Argument:
        - name: str, default 'help'
    '''
    if name in command.s:
        return command.s[name].__doc__.strip() or 'CommandHasNoDoc'
    else:
        return 'CommandNotFound'


@commander
def all():
    '''get all commands
    '''
    return '\n'.join(command.s)


@commander
def why():
    '''why
    '''
    return _why()
