from pydantic import BaseModel

import os

class Settings(BaseModel):
    swagger: dict = {
        "defaultModelsExpandDepth": -1,
    }
    url: str = os.getenv("URL")
    token: str = os.getenv("TOKEN")

settings = Settings()
