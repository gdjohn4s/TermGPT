import argparse

class Args:
    SETAPIKEY = "--setKey"


class Cli:
    def __init__(self) -> None:
        parser = argparse.ArgumentParser(description="Shell GPT Pippo")
        parser.add_argument(Args.SETAPIKEY, type=str, help="set openai api key")
        args = parser.parse_args()
        if not args:
            print("Please provide an argument, use -h or --help to get help.")

    def __add_to_config(self, config) -> None:
        pass