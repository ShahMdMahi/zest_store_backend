from pydantic_settings import BaseSettings

class APISettings(BaseSettings):
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Zest Store API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "E-commerce API for Zest Store"

    class Config:
        case_sensitive = True

api_settings = APISettings() 