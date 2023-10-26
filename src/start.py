#!/usr/bin/env python -O
from openai.error import AuthenticationError
from rich.console import Console
from src.cli import Cli


def main():
    try:
        console = Console()
        cli = Cli()
        cli.run()
    except AuthenticationError:
        console.print("Error authenticating to openai!", style="red")
        print("Did you forget to set your openai key?")


if __name__ == "__main__":
    main()
