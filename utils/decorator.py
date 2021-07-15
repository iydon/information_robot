import functools
import shlex


class command:
    s = dict()  # command.s
    t = dict()  # type

    def __init__(self, func, return_='text'):
        '''
        - Argument:
            - func: Callable
            - return_: str, in {'text', 'error'}
        '''
        self.s[func.__name__] = func
        self.t[func.__name__] = return_
        functools.wraps(func)(self)

    def __call__(self, *args, **kwargs):
        return self.__wrapped__(*args, **kwargs)

    @classmethod
    def from_str(cls, string):
        '''
        - Argument:
            - string: str
                - pattern:
                    >>> test a 'b' 'c d' 5
                    >>> test a~a b~'b b' cc~'c'

        - Return:
            - {'return': ..., 'type': ...}

        - Reference:
            - https://code.activestate.com/recipes/577122-transform-command-line-arguments-to-args-and-kwarg/
            - https://stackoverflow.com/questions/830937/python-convert-args-to-kwargs
        '''
        argv = shlex.split(string)
        if not (argv and argv[0] in cls.s):
            return {'return': 'SyntaxError', 'type': 'error'}
        func, argv, return_type = cls.s[argv[0]], argv[1:], cls.t[argv[0]]
        # transform command line arguments to args and kwarg
        args, kwargs = list(), dict()
        for arg in argv:
            if arg.count('~') >= 1:
                kwargs.__setitem__(*arg.split('~', maxsplit=1))
            else:
                args.append(arg)
        # convert args to kwargs
        kwargs.update(zip(func.__code__.co_varnames, args))
        # type cast
        for name, T in func.__annotations__.items():
            if name in kwargs:
                try:
                    kwargs[name] = T(kwargs[name])
                except Exception:  # not isinstance(T, type)
                    return {'return': 'TypeError', 'type': 'error'}
        # call
        try:
            return {'return': func(**kwargs), 'type': return_type}
        except Exception:
            return {'return': 'RuntimeError', 'type': 'error'}


def commander(func=None, return_='text'):
    if func:
        return command(func)
    else:
        def wrapper(func):
            return command(func, return_)
        return wrapper


if __name__ == '__main__':
    @commander(return_='text')
    def help(name: str = 'help'):
        '''
        get the docstring of the command `name`

        - Argument:
            - name: str, default 'help'
        '''
        if name in command.s:
            return command.s[name].__doc__ or 'CommandHasNoDoc'
        else:
            return 'CommandNotFound'

    print(command.from_str('help 404'))
