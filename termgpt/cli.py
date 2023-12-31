from termgpt.info import MD_HEADER, ALL_POSSIBLE_MODELS
from termgpt.ui.termgptUI import TermGPTUi
from termgpt.engine.termgpt import TermGPT
from rich.markdown import Markdown
from rich.console import Console
from typing import Generator
from termgpt.engine import (
    config_path,
    CONFIG_FILE,
    get_all_config,
    update_yaml_config,
    initial_config,
)
from rich.live import Live
import argparse
import yaml
import sys


class CliState:
    # TODO: change state to cli application
    STARTED = False
    EXECUTION = False
    LOADING = False
    ERROR = False
    STOPPED = False


class Args:
    """Class containing constant arguments for CLI commands."""

    SETAPIKEY = "setkey"
    PROMPT = "prompt"
    SHELL = "shell"
    GUI = "gui"
    MODELS = "models"
    RESET = "reset"


class Options:
    SET_API_KEY_OPT = "--set-key"
    SET_MODEL = "--set-model"


class Cli:
    """A command-line interface (CLI) tool for interacting with TermGPT.

    This class provides functionality to set API key, prompt ChatGPT, or use a GUI.

    Attributes:
        parser (argparse.ArgumentParser): The main argument parser.
        subparsers (argparse._SubParsersAction): Subparsers for different commands.
    """

    console = Console()

    def __init__(self):
        """Initializes the CLI tool with argument parsers and subparsers."""
        CliState.EXECUTION = True
        self.parser = argparse.ArgumentParser(
            prog="TermGPT", description="TermGPT tool made by gdjohn4s."
        )
        self.subparsers = self.parser.add_subparsers(dest="command")
        self._add_subparsers()
        self._shell_subparser()
        self._model_subparser()
        self._reset_config_subparser()

    def save_info(self, tokens_used) -> None:
        """Save the instance information to data persistence"""
        new_config = get_all_config()
        new_config["termGPT"]["token_used"] += tokens_used
        update_yaml_config(new_config=new_config)

    def _add_subparsers(self):
        """Private method to add specific command subparsers."""

        # Set api key
        set_api_key = self.subparsers.add_parser(
            Args.SETAPIKEY, help="set openai api key"
        )
        set_api_key.add_argument(
            "api_key", type=str, help="the api key generated by open ai."
        )
        set_api_key.set_defaults(func=self.set_key)

        # Gui command
        spawn_gui = self.subparsers.add_parser(Args.GUI, help="use Gui instead")
        spawn_gui.set_defaults(func=self.gui)

        # Ask chatgpt
        ask_gpt = self.subparsers.add_parser(Args.PROMPT, help="Ask chatgpt something")
        ask_gpt.add_argument("prompt", type=str, help="prompt to send to chatgpt")
        ask_gpt.set_defaults(func=self.ask_gpt)

    def _shell_subparser(self):
        """Subparser for interactive shell"""
        # Shell command
        shell = self.subparsers.add_parser(Args.SHELL, help="spawn a gpt shell")
        shell.set_defaults(func=self.shell)

    def _model_subparser(self):
        """Subparser for models commands"""
        # Model parse
        model_parser = self.subparsers.add_parser(
            Args.MODELS, help="gpt model handling"
        )
        model_list = model_parser.add_subparsers(
            dest="model_command", help="Model sub-commands"
        )

        # List for all models
        list_parser = model_list.add_parser(
            "list", help="List available models for chatGPT"
        )
        list_parser.set_defaults(func=self.spawn_model_list)

        # Set a new model
        set_model_parser = model_list.add_parser(
            "set-model", help="Set a new gpt model"
        )
        set_model_parser.add_argument(
            "model_name", type=str, help="Name of the GPT model to set as current"
        )
        set_model_parser.set_defaults(func=self.set_model)

    def _reset_config_subparser(self):
        # Reset command
        reset = self.subparsers.add_parser(Args.RESET, help="reset the configuration")
        reset.set_defaults(func=self.reset_configuration)

    # -- Cli Functions -- #
    def set_key(self, args: argparse.Namespace):
        """Set the OpenAI API key in the configuration.

        Args:
            args (argparse.Namespace): Contains the api_key attribute.
        """
        with open(f"{config_path}/{CONFIG_FILE}", "r") as nc:
            new_config = yaml.safe_load(nc)
            self.console.print(f"File {CONFIG_FILE} opened [green]Successfully[/green]")

        new_config["termGPT"]["api_key"] = args.api_key

        with open(f"{config_path}/{CONFIG_FILE}", "w") as nc:
            yaml.dump(new_config, nc, default_flow_style=False)
            self.console.print("Api key [green]imported[/green]")

    def print_response(self, response: Generator):
        """
        Renders Markdown content in real-time from a character generator to the console.

        This function takes a generator that yields Markdown-formatted characters one at a time.
        It progressively builds the Markdown content and uses the Rich library's Live object to render
        it in the console. The rendering is updated in real-time with each new character received.

        The Live object ensures that the output is displayed within the terminal's visible area
        and overwrites the previous content smoothly, creating an animation effect as the content appears character by character.

        Parameters:
        - response (Generator): A generator object that yields characters of the Markdown content.

        The function handles KeyboardInterrupt to allow the user to stop the rendering process cleanly.
        At the end of the function, or if interrupted, it flushes the system's stdout buffer to ensure all content is written to the terminal.

        Example usage:
        >>> response_generator = (char for char in "# Hello, World!")
        >>> your_class_instance = YourClassName()
        >>> your_class_instance.print_response(response_generator)

        Note: This function is designed to be a method of a class that contains a 'console' attribute initialized with Rich's Console class.
        """
        markdown_content = ""

        # Using conresponse to manage the Live object
        with Live(
            console=self.console, auto_refresh=False, vertical_overflow="visible"
        ) as live:
            try:
                for char in response:
                    markdown_content += char
                    content = Markdown(markdown_content)

                    # Update the live object
                    live.update(content)
                    live.refresh()

            except KeyboardInterrupt:
                # Allow clean exit on user interrupt
                pass
            finally:
                # Ensure the terminal's buffer is flushed
                sys.stdout.flush()

    def ask_gpt(self, args: argparse.Namespace):
        """Prompt ChatGPT and display the response.

        Args:
            args (argparse.Namespace): Contains the prompt attribute.
        """
        gpt = TermGPT()
        response = gpt.run(args.prompt, stream=True)
        parsed_response = gpt.parse_chat_content(response, stream=True)

        print(gpt.total_tokens_used)
        # self.save_info(tokens_used)

        self.console.print("TermGPT: ", end="", style="green")
        self.print_response(parsed_response)

        CliState.EXECUTION = False
        exit(0)

    def shell(self, args: argparse.Namespace):
        md_head = Markdown(MD_HEADER)
        self.console.print(md_head)

        while CliState.EXECUTION:
            prompt = input("TermGPT> ")
            print("interactive shell coming soon!")

    def gui(self, args: argparse.Namespace = None):
        """Run the GUI version of TermGPT."""
        term_gui = TermGPTUi()
        term_gui.run()

    def spawn_model_list(self, args: argparse.Namespace = None):
        print("Models Available:")
        config = get_all_config()
        model_selected = config["termGPT"]["model"]
        for model in ALL_POSSIBLE_MODELS:
            if model_selected == model:
                self.console.print(f"[yellow]{model}[/yellow] (Actual Selected)")
            else:
                self.console.print(f"[green]{model}[/green]")

    def set_model(self, args):
        if args.model_name not in ALL_POSSIBLE_MODELS:
            self.console.print(
                f"[red]ERROR!![/red] The model [bold]{args.model_name}[/bold] is not present on our available models!"
            )
            print("Choose one from this list instead!")

            for model in ALL_POSSIBLE_MODELS:
                self.console.print(f"[green]{model}[/green]")
            exit(1)
        config = get_all_config()
        config["termGPT"]["model"] = args.model_name
        update_yaml_config(new_config=config)
        self.console.print(f"Chosen model: [bold]{args.model_name.capitalize()}[/bold]")

    def reset_configuration(self, args=None):
        update_yaml_config(new_config=initial_config)
        self.console.print("Configuration [green]initialized[/green]")

    def run(self):
        """Parse the arguments and execute the corresponding command."""
        args = self.parser.parse_args()
        if args.command is None or args is None:
            self.parser.print_help()
        else:
            try:
                args.func(args)
            except AttributeError as e:
                print(e)
                self.parser.print_help()
