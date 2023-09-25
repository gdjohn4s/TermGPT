from engine import _config_path
import yaml


class Config:
    LOCAL_CONFIG_PATH: str = str()
    SHELL_GPT_API_KEY: str = str()
    SHELL_GPT_TOKEN_USED: int = int()

    def __init__(self) -> None:
       super().__init__()

    def parse_config(self) -> dict:
        with open(_config_path, 'r') as cf:
            return yaml.safe_load(cf)
