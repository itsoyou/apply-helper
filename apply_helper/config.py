import logging
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Config:
    UPLOAD_FOLDER = "uploads"
    DEBUG = True
    ALLOWED_EXTENTIONS = {"pdf"}
    ASSISTANT_ID: str = ""
    THREAD_ID: str = ""
    if os.getenv("OPENAI_API_KEY") and isinstance(
        os.getenv("OPENAI_API_KEY"), str
    ):
        CLIENT = OpenAI()
        CLIENT.api_key = os.getenv("OPENAI_API_KEY")
    else:
        logger.error("OPEN API KEY does not exists")
