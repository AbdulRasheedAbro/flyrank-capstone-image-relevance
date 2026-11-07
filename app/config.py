from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    ollama_base_url: str = "http://localhost:11434"
    ollama_vision_model: str = "llava"
    ollama_embed_model: str = "all-minilm"
    vision_confidence_threshold: float = 0.70
    similarity_threshold: float = 0.65
    max_retries: int = 3
    batch_size: int = 20
    mock_ai: bool = False

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
