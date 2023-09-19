from dotenv import load_dotenv
import logging
import os

load_dotenv()

logging.basicConfig(filename='shellGPT.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("ShellGPT Engine started")

assert os.getenv("API_KEY") != "<YOUR_API_KEY>", "Please enter your API key"