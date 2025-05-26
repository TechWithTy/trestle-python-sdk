from pydantic import BaseSettings, Field


class TrestleConfig(BaseSettings):
    """
    Configuration for Trestle API client.
    """
    api_key: str = Field(..., env="TRESTLE_API_KEY")
    base_url: str = Field("https://api.trestle.io/v1", env="TRESTLE_BASE_URL")
    timeout: float = Field(30.0, env="TRESTLE_TIMEOUT")
    max_retries: int = Field(3, env="TRESTLE_MAX_RETRIES")

    class Config:
        env_file = ".env"
