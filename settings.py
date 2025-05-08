from pydantic import BaseModel

import os

class Settings(BaseModel):
    swagger: dict = {
        "defaultModelsExpandDepth": -1,
    }
    url: str = os.getenv("URL")
    token: str = os.getenv("TOKEN")
    users: list[int] = [1093286245, 507330315]

settings = Settings()
