# settings.py

from dotenv import load_dotenv
import os
# load_dotenv()


from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


print(os.getenv("APP_SETTINGS"))