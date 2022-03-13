from pydantic import BaseSettings

class Settings(BaseSettings):
    NOTION_TOKEN: str = ""
    WEBHOOK_ID: str = ""
    WEBHOOK_TOKEN: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        fields = {
            "NOTION_TOKEN": {"env": ["TOKEN", "TOKEN_KEY"]},
            "WEBHOOK_ID": {"env": ["WEBHOOK_ID"]},
            "WEBHOOK_TOKEN": {"env": ["WEBHOOK_TOKEN"]},
        }
