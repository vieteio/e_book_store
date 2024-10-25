from pydantic import BaseSettings

class Settings(BaseSettings):
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    S3_BUCKET: str
    MONGODB_URI: str
    POSTGRESQL_URI: str

    class Config:
        env_file = ".env"

settings = Settings()
