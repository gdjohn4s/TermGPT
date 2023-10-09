#!/usr/bin/env python -O
from ui.termgptUI import TermGPTUi
from cli import Cli

if __name__ == '__main__':
    cli = Cli()
    app = TermGPTUi()
    app.run()
