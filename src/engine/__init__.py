from _info import initial_config
from dotenv import load_dotenv
import platform
import logging
import yaml
import os

load_dotenv()

logging.basicConfig(filename='shellGPT.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("Checking configuration")

_CONFIG_FILE: str = "config.yaml"
_home: str = str()
_config_path: str = str()
_os: str = platform.system()


def check_config_path() -> bool:
    return True if os.path.exists(_config_path) and os.path.isdir(_config_path) else False


def create_yaml_config() -> None:
    if check_config_path():
        if not os.path.exists(f"{_config_path}/{_CONFIG_FILE}"):
            logging.info(f"Creating {_CONFIG_FILE} file")
            with open(f"{_config_path}/{_CONFIG_FILE}", "w+") as cf:
                yaml.dump(initial_config, cf, default_flow_style=False)
                return
        return
    os.mkdir(_config_path)
    create_yaml_config()


if _os == "Windows":
    # TODO: Windows Path configuration file
    # Win: C:\
    print("Windows")
    _home = os.environ['USERPROFILE']
elif _os == "Darwin":
    _home = os.getenv("HOME")
    _config_path = rf"{_home}/.config/shellGPT"
elif _os == "Linux":
    _home = os.getenv("HOME")
    _config_path = rf"{_home}/.config/shellGPT"
else:
    logging.error("{} os error".format(_os))
    raise OSError

logging.info("{} operating system detected".format(_os))
create_yaml_config()

# TODO: Edit assert to new configuration logic
assert os.getenv("API_KEY") != "<YOUR_API_KEY>", "Please enter your API key"

__all__ = [
    _os,
    _home,
    _config_path
]