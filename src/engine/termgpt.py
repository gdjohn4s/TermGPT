# termgpt.py
import openai
import time
import sys


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

    def __init__(self, model="gpt-3.5-turbo", role="user"):
        self.model = model
        self.role = role
        self.delay = 0.01
        self.total_tokens_used = 0

    def increment_and_get_tokens(self, text) -> int:
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
        assert isinstance(text, dict)
        tokens: int = text.get("usage", "").get("total_tokens", "")
        self.total_tokens_used += tokens
        return self.total_tokens_used

    def simulate_typing(self, text):
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

    def parse_chat_content(self, text) -> str:
        """
        Parse the openai API response to get the content result

        ...

        Attributes
        ----------
        text : Any | Literal['']
        """
        assert isinstance(text, dict)
        choices = text.get("choices", [])
        return choices[0].get("message", {}).get("content", "") if choices else ""

    def run(self, content) -> dict:
        """
        Run the engine calling openai API to use chatGPT

        ...

        Attributes
        ----------
        content : str
        """
        chat_completion = openai.ChatCompletion.create(
            model=self.model, messages=[{"role": self.role, "content": content}]
        )
        return chat_completion
