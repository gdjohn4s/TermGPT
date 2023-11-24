# informations and constants
from typing import Union
# from src.engine import _config_path, _CONFIG_FILE

CLI_HEADER: str = """
████████╗███████╗██████╗░███╗░░░███╗░██████╗░██████╗░████████╗
╚══██╔══╝██╔════╝██╔══██╗████╗░████║██╔════╝░██╔══██╗╚══██╔══╝
░░░██║░░░█████╗░░██████╔╝██╔████╔██║██║░░██╗░██████╔╝░░░██║░░░
░░░██║░░░██╔══╝░░██╔══██╗██║╚██╔╝██║██║░░╚██╗██╔═══╝░░░░██║░░░
░░░██║░░░███████╗██║░░██║██║░╚═╝░██║╚██████╔╝██║░░░░░░░░██║░░░
░░░╚═╝░░░╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝░╚═════╝░╚═╝░░░░░░░░╚═╝░░░
"""

MD_HEADER: str = """
# Welcome to termgpt!

Hello there! 👋 We're thrilled to have you onboard. 
If you have any questions or need assistance, feel free to ask. 
Let's make your terminal experience amazing!
"""

initial_config: dict[str, Union[int, str]] = {
    "local": {"configuration_path": ""},
    "termGPT": {"api_key": "", "model": "gpt-3.5-turbo", "token_used": 0},
}

ALL_POSSIBLE_MODELS = [
    "gpt-4",
    "gpt-3.5-turbo",
    "text-davinci-003",
    "code-davinci-002",
    "dall-e-3",
    "tts-1",
    "babbage-002",
    "davinci-002",
]
