import functools
import shlex


class command:
    s = dict()  # command.s

    def __init__(self, func):
        self.s[func.__name__] = func
        functools.wraps(func)(self)

    def __call__(self, *args, **kwargs):
        return self.__wrapped__(*args, **kwargs)

    @classmethod
    def from_str(cls, string):
        '''
        Argument:
            - string: str
                - pattern:
                    >>> test a 'b' 'c d' 5
                    >>> test a~a b~'b b' cc~'c'

        Return:
            - str

        Reference:
            - https://code.activestate.com/recipes/577122-transform-command-line-arguments-to-args-and-kwarg/
            - https://stackoverflow.com/questions/830937/python-convert-args-to-kwargs
        '''
        argv = shlex.split(string)
        if not (argv and argv[0] in cls.s):
            return 'SyntaxError'
        func, argv = cls.s[argv[0]], argv[1:]
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
                    return 'TypeError'
        # call
        try:
            return str(func(**kwargs))
        except Exception:
            return 'RuntimeError'


if __name__ == '__main__':
    @command
    def help(name: str = 'help'):
        '''help me
        '''
        if name in command.s:
            return command.s[name].__doc__ or 'CommandHasNoDoc'
        else:
            return 'CommandNotFound'

    print(command.from_str('help 404'))
