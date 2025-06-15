import os

from dotenv import load_dotenv

load_dotenv()


def get_env_var(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


ORACLE_USER = get_env_var("ORACLE_USER")
ORACLE_PASSWORD = get_env_var("ORACLE_PASSWORD")
ORACLE_DSN = get_env_var("ORACLE_DSN")
