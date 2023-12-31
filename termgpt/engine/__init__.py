from termgpt.info import initial_config
from dotenv import load_dotenv
from datetime import datetime
import platform
import logging
import yaml
import os

load_dotenv()

# TODO: Consider using .local instead of .config directory

logging.basicConfig(
    filename="termGPT.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logging.info("Checking configuration")

CONFIG_FILE: str = "config.yaml"
config_path: str = str()

_home: str = str()
_os: str = platform.system()


def checkconfig_path() -> bool:
    return True if os.path.exists(config_path) and os.path.isdir(config_path) else False


def create_yaml_config() -> None:
    if checkconfig_path():
        if not os.path.exists(f"{config_path}/{CONFIG_FILE}"):
            logging.info(f"Creating {CONFIG_FILE} file")

            with open(f"{config_path}/{CONFIG_FILE}", "w+") as cf:
                initial_config["local"]["configuration_path"] = config_path  # type: ignore
                yaml.dump(initial_config, cf, default_flow_style=False)
                return

        return

    os.mkdir(config_path)
    create_yaml_config()


def update_yaml_config(new_config: dict[str, int | str]):
    if datetime.now().day == 1:
        new_config = initial_config["termGPT"]["tokens"] = 0  # type: ignore

    with open(f"{config_path}/{CONFIG_FILE}", "w+") as nc:
        yaml.dump(new_config, nc, default_flow_style=False)


def get_all_config():
    with open(f"{config_path}/{CONFIG_FILE}", "r") as cfg:
        yaml_config = yaml.safe_load(cfg)
        return yaml_config


def get_tokens_from_yaml() -> int:
    with open(f"{config_path}/{CONFIG_FILE}", "r") as cfg:
        tmp_yaml = yaml.safe_load(cfg)
        return tmp_yaml["termGPT"]["token_used"]


def is_apikey_configured() -> bool:
    with open(f"{config_path}/{CONFIG_FILE}", "r") as cfg:
        tmp_yaml = yaml.safe_load(cfg)
        api_key: str = tmp_yaml["termGPT"]["api_key"]

        return api_key != ""


def get_api_key() -> str:
    with open(f"{config_path}/{CONFIG_FILE}", "r") as cfg:
        tmp_yaml = yaml.safe_load(cfg)
        api_key: str = tmp_yaml["termGPT"]["api_key"]

        return api_key


if _os == "Windows":
    # TODO: Windows Path configuration file
    # Win: C:\
    print("Windows")
    _home = os.environ["USERPROFILE"]
elif _os == "Darwin":
    _home = os.getenv("HOME")  # type: ignore
    config_path = rf"{_home}/.config/termGPT"
elif _os == "Linux":
    _home = os.getenv("HOME")  # type: ignore
    config_path = rf"{_home}/.config/termGPT"
else:
    logging.error("{} os error".format(_os))
    raise OSError

logging.info("{} operating system detected".format(_os))
create_yaml_config()
