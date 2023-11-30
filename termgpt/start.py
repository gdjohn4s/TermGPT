#!/usr/bin/env python -O
from openai.error import AuthenticationError
from rich.console import Console
from termgpt.info import CLI_HEADER
from termgpt.cli import Cli


def main():
    try:
        console = Console()
        cli = Cli()
        cli.run()
    except AuthenticationError:
        console.print("Error authenticating to openai!", style="red")
        print("Did you forget to set your openai key?")
    except KeyboardInterrupt:
        print(CLI_HEADER)
        console.print("Thanks for using [green]TermGPT![/green]")


if __name__ == "__main__":
    main()
