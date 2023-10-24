# termgptUI.py
from textual.containers import ScrollableContainer
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.binding import Binding
from engine.termgpt import TermGPT
from textual.widget import Widget
from dotenv import load_dotenv
from textual.widgets import (
    MarkdownViewer,
    Markdown,
    Footer,
    Input,
    Tabs,
)
from datetime import datetime
from textual import on
from enum import Enum
import openai
import os

from _info import initial_config
from engine import (
    update_yaml_config,
    get_tokens_from_yaml,
)

load_dotenv()  # Load environment variables
openai.api_key = os.getenv("API_KEY")
date = lambda: datetime.now().strftime("%H:%M:%S")


def compose_md_view(md: str) -> ComposeResult:
    yield MarkdownViewer()


def get_pages_content(page: list) -> str:
    content: str = ""
    for sentence in page:
        content += f"{sentence}\n\n"

    return content


class TermGPTState(Enum):
    START: str = "start"
    MIDDLE: str = "middle"


class UpdateTokens(Widget):
    """Represent the total token used for one istance."""

    ref_tokens = reactive(0)
    ref_monthly_tokens = reactive(get_tokens_from_yaml())

    def update(self, token):
        self.ref_tokens = token

    def get_tokens(self) -> int:
        return self.ref_tokens

    def render(self) -> str:
        return f"Session tokens used: {self.ref_tokens} | Monthly tokens used: {self.ref_monthly_tokens}"


class TermGPTUi(App):
    """
    This class represents the termGPT UI.

    All widgets logic will be described here.
    """

    GREETINGS: str = f"[{date()}] Hi {os.getenv('USER')}! Welcome in termGPT\n Please insert an input to start using me"

    CSS = """
   Tabs {
      dock: top;
   }
   Screen {
      align: center middle;
   }
   Label {
      margin: 0 5 0 0;
   }
   Markdown {
      margin: 1 1;
      padding: 0 2;
      width: 100%;
      height: 100%;
      border: tall $primary;
      content-align: left bottom;
   }
   ScrollableContainer {
      height: 90%;
   }
   Input {
      margin: 0 0;
   }
   UpdateTokens {
      height: 3%;
   }
   """

    BINDINGS = [
        ("a", "add", "Add tab"),
        ("r", "remove", "Remove active tab"),
        ("c", "clear", "Clear tabs"),
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(key="C-v", action="copy", description="Copy the code"),
    ]

    md_pages: list[list[str]] = []
    md_responses: list[str] = []
    md_gpt_actual_response: str = None
    tab_id: int = 0

    def __init__(self):
        super().__init__()
        self.ui_states = TermGPTState.START
        self.tabs_counter = 0
        self.termGPT = TermGPT()
        self.md = Markdown()
        self.tokens = UpdateTokens()
        self.vertical_scroll = ScrollableContainer(self.md)

    def get_tokens_used(self) -> int:
        return self.tokens.ref_tokens

    def _save_info(self) -> None:
        """Save the instance information to data persistence"""
        updated_tokens = self.tokens.ref_monthly_tokens + self.get_tokens_used()
        new_config = initial_config
        new_config["termGPT"]["token_used"] = updated_tokens
        update_yaml_config(new_config=new_config)

    def compose(self) -> ComposeResult:
        """Create the components using textual Widgets"""
        yield Tabs(f"New tab #{self.tabs_counter}")
        yield self.vertical_scroll
        yield Input(placeholder="TermGPT> ")
        yield self.tokens
        yield Footer()

    def action_add(self) -> None:
        """Add a new tab."""
        if self.tabs_counter >= 8:
            return

        tabs = self.query_one(Tabs)
        self.md_pages.append(self.md_responses)
        self.md_responses = []
        self.tabs_counter += 1
        self.tab_id += 1
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

    def on_mount(self):
        """Set the pointer widget to focus"""
        self.query_one(Tabs).focus()

    @on(Tabs.TabActivated)
    def handle_history_and_new_tabs(self, event: Tabs.TabActivated):
        """
        This function is triggered when the user switch between tabs.

        It updates the tab page content restoring tab data using tab id.
        """
        md_tab = self.query_one(Markdown)
        if event.tab is None:
            md_tab.visible = False
        else:
            md_tab.visible = True
            if len(self.md_responses) == 0:
                self.md_responses.append(self.GREETINGS)
                md_tab.update(self.GREETINGS)
                return

            self.tab_id: int = int(event.tab.id.replace("tab-", "")) - 1
            if self.tab_id == 0 and self.ui_states == TermGPTState.START:
                return

            restored_page = get_pages_content(self.md_pages[self.tab_id])
            md_tab.update(restored_page)

    @on(Input.Submitted)
    async def send_to_chatgpt(self, event: Input.Submitted):
        """
        This function is triggered on Input.Submitted event.

        Run the termGPT engine calling openAI API and update the Markdown widget on the Terminal.
        """
        if self.ui_states != TermGPTState.MIDDLE:
            self.ui_states = TermGPTState.MIDDLE

        if event.value:
            gpt_content: dict = self.termGPT.run(event.value)
            self.md_gpt_actual_response: str = (
                f"[{date()}] {self.termGPT.parse_chat_content(gpt_content)}"
            )
            self.md_responses.append(self.md_gpt_actual_response)

            if len(self.md_pages) == 0:
                self.md_pages.append(self.md_responses)
            else:
                self.md_pages[self.tab_id].append(self.md_responses[-1])

            self.tokens.update(self.termGPT.increment_and_get_tokens(gpt_content))
            self.md.update(markdown=self.md_gpt_actual_response)
            self.md_responses = []
            self._save_info()
