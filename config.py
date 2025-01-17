from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    BOT_TOKEN: str

    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    class Config:
        env_file = ".env"
        extra = "ignore"
        env_ignore_empty = True


settings = Settings()
