# shellgpt.py
import openai
import time
import sys


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
   BINDINGS = [
      ("t", "toggle_table_of_contents", "TOC"),
      ("b", "back", "Back"),
      ("f", "forward", "Forward"),
      ("q", "quit", "Exit")
    ]

   def __init__(self, model="gpt-3.5-turbo", role="user"):
      self.model = model
      self.role = role
      self.delay = 0.01

   def simulate_typing(self, text):
      self.delay = 0.007 if 100 < len(text) < 250 else 0.004
      for char in text:
         sys.stdout.write(char)
         sys.stdout.flush()
         time.sleep(self.delay)

   def parse_chat_content(self, text):
      choices = text.get("choices", [])
      return choices[0].get("message", {}).get("content", "") if choices else ""

   def run(self, content):
      chat_completion = openai.ChatCompletion.create(
         model=self.model, messages=[{"role": self.role, "content": content}]
      )
      return chat_completion
