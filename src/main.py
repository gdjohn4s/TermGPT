#!/usr/bin/env python -O

from ui.shellgptUI import ShellGPTUi
from cli import Cli

if __name__ == '__main__':
    cli = Cli()
    app = ShellGPTUi()
    app.run()
