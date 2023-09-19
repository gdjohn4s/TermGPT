#!/usr/bin/env python -O

from textual.widgets import Footer, Label, Tabs, Input, Markdown, Button
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.binding import Binding
from textual import on

from dotenv import load_dotenv

import openai
import time
import sys
import os


class ShellGPT:
    """
    This class represents the ShellGPT engine. Here you will find all the necessary methods to
    make a call and parse GPT responses.

    ...

    Attributes
    ----------
    model : str
        the model you want to use like: gpt-3.5-turbo

    """

    load_dotenv()  # load the environment variables
    openai.api_key = os.getenv("API_KEY")  # set the API Key

    # default private properties
    __user = os.getenv("USER")
    __role = "user"
    __delay = 0.01  # default delay for typing effect

    # public properties
    model = "gpt-3.5-turbo"
    total_tokens_used = 0

    def __init__(self, model="gpt-3.5-turbo", __role="user") -> None:
        self.model = model
        self.__role = __role

    def simulate_typing(self, text) -> None:
        if len(text) > 100 and len(text) < 250:
            self.__delay = 0.007
        elif len(text) > 250:
            self.__delay = 0.004

        print(len(text))
        print(self.__delay)

        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(self.__delay)

    def increment_tokens(self, text) -> None:
        assert isinstance(text, dict)
        tokens: int = text.get("usage", "").get("total_tokens", "")
        self.total_tokens_used += tokens

    def parse_chat_content(self, text: dict) -> str:
        assert isinstance(text, dict)
        choices: list = text.get("choices")

        if choices and len(choices) > 0:
            # self.increment_tokens(text)
            return choices[0].get("message", {}).get("content", "")
        return ""

    def run(self, content):
        '''
        Sends the content to chatGPT and get the response.

            Parameters:
                    content (str): Text to send to chatGPT

            Returns:
                    None

            Example:
            ```
            content: str = "Hi ChatGPT, how's going?"
            engine: ShellGPT = ShellGPT()
            engine.run(content)
            ```
        '''
        chat_completion = openai.ChatCompletion.create(
            model=self.model, messages=[{"role": self.__role, "content": content}])
        return chat_completion
        # print(chat_completion)
        # self.simulate_typing(self.parse_chat_content(chat_completion))


class ShellGPTUi(App):

    CSS = """
    Tabs {
        dock: top;
    }
    Screen {
        align: center middle;
    }
    Markdown {
        margin:1 1;
        width: 100%;
        height: 85%;
        border: tall $primary;
        content-align: left bottom;
    }
    """

    tabs_counter = 0
    shellGPT = ShellGPT()
    md = Markdown()

    BINDINGS = [
        ("a", "add", "Add tab"),
        ("r", "remove", "Remove active tab"),
        ("c", "clear", "Clear tabs"),
        Binding(key="q", action="quit", description="Quit the app"),

    ]

    def compose(self) -> ComposeResult:
        yield Tabs(f"New tab #{self.tabs_counter}")
        yield self.md
        yield Input(placeholder="ShellGPT> ")
        # with Horizontal():
        #     yield Input(placeholder="ShellGPT> ")
        #     yield Label()
        yield Footer()

    def on_mount(self) -> None:
        """Focus the tabs when the app starts."""
        self.query_one(Tabs).focus()

    def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
        """Handle TabActivated message sent by Tabs."""
        label = self.query_one(Markdown)
        if event.tab is None:
            # When the tabs are cleared, event.tab will be None
            label.visible = False
        else:
            label.visible = True
            label.update(
                f" Hi {os.getenv('USER')}! Welcome in shellGPT\n Please insert an input to start using me")

    def action_add(self) -> None:
        """Add a new tab."""
        tabs = self.query_one(Tabs)
        self.tabs_counter += 1
        tabs.add_tab(f"New tab #{self.tabs_counter}")

    def action_remove(self) -> None:
        """Remove active tab."""
        tabs = self.query_one(Tabs)
        active_tab = tabs.active_tab
        if active_tab is not None:
            tabs.remove_tab(active_tab.id)

    def action_clear(self) -> None:
        """Clear the tabs."""
        self.query_one(Tabs).clear()

    @on(Input.Submitted)
    def send_to_chatgpt(self, event: Input.Submitted):
        if event.value:
            gpt_content = ShellGPT.run(ShellGPT, content=event.value)
            gpt_parsed = ShellGPT.parse_chat_content(
                ShellGPT, text=gpt_content)
            self.md.update(markdown=gpt_parsed)
        print("Input submitted")


if __name__ == '__main__':
    app = ShellGPTUi()
    app.run()
