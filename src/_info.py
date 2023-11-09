# informations and constants
from typing import Union

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
    "termGPT": {"api_key": "", "token_used": 0},
}
