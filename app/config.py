import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    MAX_WEBSITES = 10

    REQUEST_TIMEOUT = 30

    OUTPUT_DIR = "app/output"

    RAW_HTML_DIR = "app/output/raw_html"

    CLEAN_TEXT_DIR = "app/output/cleaned_text"

    EXTRACTED_DATA_DIR = "app/output/extracted_data"

    ANALYSIS_DIR = "app/output/analysis"

    PROPOSAL_DIR = "app/output/proposals"

    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/138.0 Safari/537.36"
    )


    MODEL_NAME = "qwen2.5:1.5b"

MAX_CONTENT_LENGTH = 12000

OUTPUT_FOLDER = "output"