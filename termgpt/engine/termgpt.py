# termgpt.py
from typing import Generator, Any, TypedDict, cast
from src.engine import get_all_config
from enum import Enum
import openai
import time
import sys


class TermGPTState(Enum):
    CLI_MODE = False
    IS_LOADING = False


class TermGPTConfig(TypedDict):
    model: str
    role: str
    delay: float
    token_used: int


class TermGPT:
    """
    This class represents the TermGPT engine. Here you will find all the necessary methods to
    make a call and parse GPT responses.

    ...

    Attributes
    ----------
    model : str
       the model you want to use like: gpt-3.5-turbo

    """

    config = get_all_config()

    def __init__(self):
        self.model: str = self.config["termGPT"]["model"]
        self.role: str = self.config["termGPT"]["role"]
        self.delay: float = self.config["termGPT"]["delay"]
        self.total_tokens_used: int = self.config["termGPT"]["token_used"]

    def increment_and_get_tokens(self, text: Any) -> int | float:
        """
        Update the total tokens used and returns it

        ...

        Attributes
        ----------
        text : dict

        Returns
        ----------
        tokens : int
        """
        tokens: str = text.get("usage", "").get("total_tokens", "")
        if tokens:
            self.total_tokens_used += tokens
        return self.total_tokens_used

    def simulate_typing(self, text: Any):
        """
        Apply the chatGPT text effect to a string

        ...

        Attributes
        ----------
        text : str
        """
        self.delay = 0.007 if 100 < len(text) < 250 else 0.004
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(self.delay)

    def parse_chat_content(self, text: Generator, stream: bool) -> Generator:
        """
        Parse the openai API response to get the content result

        ...

        Attributes
        ----------
        text : Generator
        """
        response_iterator = cast(Any, text)

        if stream:
            for resp in response_iterator:
                print(resp)
                next = resp["choices"][0]
                if next["finish_reason"] is None and "content" in next["delta"]:
                    yield next["delta"]["content"]
        else:
            next = response_iterator["choices"][0]
            yield next["message"]["content"]

    def run(self, content: str, stream: bool) -> Generator:
        """
        Run the engine calling openai API to use chatGPT

        ...

        Attributes
        ----------
        content : str
        """
        chat_completion = openai.ChatCompletion.create(
            model=self.model,
            stream=stream,
            messages=[{"role": self.role, "content": content}],
        )
        return chat_completion
