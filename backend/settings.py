from dotenv import load_dotenv
import os
load_dotenv()

DB_PATH = os.environ.get("DB_PATH")
DB_TEST_PATH = os.environ.get("DB_TEST_PATH")