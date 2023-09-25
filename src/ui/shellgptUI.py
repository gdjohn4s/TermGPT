# shellgptui.py
from textual.containers import ScrollableContainer
from textual.app import App, ComposeResult
from textual.reactive import reactive
from engine.shellgpt import ShellGPT
from textual.binding import Binding
from textual.widget import Widget
from dotenv import load_dotenv
from textual.widgets import (
   MarkdownViewer,
   Markdown,
   Footer,     
   Label,
   Input, 
   Tabs, 
) 
from textual import on
import atexit
import openai
import os


load_dotenv()  # Load environment variables
openai.api_key = os.getenv("API_KEY")


def __save_info() -> None:
   """Save the instance information to data persistence"""
   # TODO: Implement this
   print("TEST INFO")


atexit.register(__save_info)


class UpdateTokens(Widget):
   """Represent the total token used for one istance."""

   ref_tokens = reactive(0)

   def update(self, token):
      self.ref_tokens = token

   def render(self) -> str:
      return f"Tokens used: {self.ref_tokens}"


class ShellGPTUi(App):
   """
   This class represents the ShellGPT UI. 
   
   All widgets logic will be described here.
   """

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
      width: 100%;
      height: 100%;
      border: tall $primary;
      content-align: left bottom;
   }
   ScrollableContainer {
      height: 90%;
   }
   UpdateTokens {
      height: 3%;
   }
   """

   BINDINGS = [
      ("a", "add", "Add tab"),
      ("r", "remove", "Remove active tab"),
      ("c", "clear", "Clear tabs"),
      Binding(key="C-v", action="quit", description="Copy the code"),
      Binding(key="q", action="quit", description="Quit the app"),
    ]

   def __init__(self):
      super().__init__()
      self.tabs_counter = 0
      self.shellGPT = ShellGPT()
      self.md = Markdown()
      self.tokens = UpdateTokens()
      self.vertical_scroll = ScrollableContainer(
         self.md
      )

   def compose(self) -> ComposeResult:
      """Create the components using textual Widgets"""
      yield Tabs(f"New tab #{self.tabs_counter}")
      yield self.tokens
      yield self.vertical_scroll
      yield Input(placeholder="ShellGPT> ")
      yield Footer()

   def compose_md_view(self, md: str) -> ComposeResult:
      yield MarkdownViewer()

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

   def on_mount(self):
      """Set the pointer widget to focus"""
      self.query_one(Tabs).focus()

   def on_tabs_tab_activated(self, event):
      """Logic on tab activated"""
      label = self.query_one(Markdown)
      if event.tab is None:
         label.visible = False
      else:
         label.visible = True
         label.update(
               f" Hi {os.getenv('USER')}! Welcome in shellGPT\n Please insert an input to start using me"
         )

   @on(Input.Submitted)
   def send_to_chatgpt(self, event):
      """
      This function is triggered on Input.Submitted event.

      Run the shellGPT engine calling openAI API and update the Markdown widget on the Terminal.
      """
      if event.value:
         gpt_content = self.shellGPT.run(event.value)
         gpt_parsed = self.shellGPT.parse_chat_content(gpt_content)
         self.tokens.update(self.shellGPT.increment_and_get_tokens(gpt_content))
         self.md.update(markdown=gpt_parsed)
