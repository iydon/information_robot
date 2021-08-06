import base64
import json
import os
import pyperclip

from prompt_toolkit import PromptSession, print_formatted_text
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.formatted_text import AnyFormattedText, HTML
from prompt_toolkit.key_binding import KeyBindings, KeyBindingsBase
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from prompt_toolkit.keys import Keys
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.shell import BashLexer


def _prompt_continuation(
    width: int, line_number: int, is_soft_wrap: bool
) -> AnyFormattedText:
    return HTML('<green>{}</green>').format('...: '.rjust(width))

def _bind() -> KeyBindingsBase:
    bindings = KeyBindings()
    self = globals()
    for key, value in self.items():
        if key.startswith('_bind_'):
            keys = key[6:].split('_')  # remove '_bind_'
            bindings.add(*(Keys[key] for key in keys))(value)
    return bindings

def _bind_Escape_Enter(event: KeyPressEvent) -> None:
    # 手动追加新行：Escape + Enter
    event.current_buffer.insert_text('\n')

def _bind_Enter(event: KeyPressEvent) -> None:
    event.current_buffer.validate_and_handle()

def _run(statement: str, encoding: str = 'utf-8') -> str:
    if statement:  # 有输入
        result = base64.b64encode(statement.encode(encoding)).decode(encoding)
        pyperclip.copy(f'/cmd {result}')
        return ''
    else:  # 无输入
        width = os.get_terminal_size().columns
        result = json.loads(base64.b85decode(pyperclip.paste().strip()))
        return f'''
{" STDOUT ":=^{width}}
{result["o"]}

{" STDERR ":=^{width}}
{result["e"]}
        '''


if __name__ == '__main__':
    session = PromptSession(
        lexer=PygmentsLexer(BashLexer), completer=WordCompleter({}, ignore_case=False),
        complete_while_typing=False, key_bindings=_bind(),
        multiline=True, prompt_continuation=_prompt_continuation,
    )
    count = 0
    while True:
        try:
            text = session.prompt(
                HTML('<green>{}</green>').format(f'In [{count}]: ')
            ).strip()
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        else:
            count += 1
            print_formatted_text(_run(text), end='\n\n')
