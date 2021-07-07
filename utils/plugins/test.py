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


# @commander(return_='image')
# def heatmap(name: str = 'dust2'):
#     '''get the heatmap by `name`

#     Argument:
#         - name: str, in {
#                 cache, dust2, mirage, overpass, vertigo, 
#                 cobblestone, inferno, nuke, train,
#             }
#     '''
#     path = os.path.join('cache', f'{name}.png')
#     assert os.path.exists(path)
#     return path
