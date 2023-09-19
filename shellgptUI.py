# shellgptui.py
from textual.app import App, ComposeResult
from textual.binding import Binding
from dotenv import load_dotenv
from shellgpt import ShellGPT
from textual.widgets import (
   Markdown, 
   Footer,     
   Input, 
   Tabs, 
) 
from textual import on
import openai
import os


load_dotenv()  # Load environment variables
openai.api_key = os.getenv("API_KEY")


class ShellGPTUi(App):
   CSS = """
   Tabs {
      dock: top;
   }
   Screen {
      align: center middle;
   }
   Markdown {
      margin: 1 1;
      width: 100%;
      height: 85%;
      border: tall $primary;
      content-align: left bottom;
   }
   """

   BINDINGS = [
      ("a", "add", "Add tab"),
      ("r", "remove", "Remove active tab"),
      ("c", "clear", "Clear tabs"),
      Binding(key="q", action="quit", description="Quit the app"),
    ]

   def __init__(self):
      super().__init__()
      self.tabs_counter = 0
      self.shellGPT = ShellGPT()
      self.md = Markdown()

   def compose(self) -> ComposeResult:
      yield Tabs(f"New tab #{self.tabs_counter}")
      yield self.md
      yield Input(placeholder="ShellGPT> ")
      yield Footer()

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
      self.query_one(Tabs).focus()

   def on_tabs_tab_activated(self, event):
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
      if event.value:
         gpt_content = self.shellGPT.run(event.value)
         gpt_parsed = self.shellGPT.parse_chat_content(gpt_content)
         self.md.update(markdown=gpt_parsed)
