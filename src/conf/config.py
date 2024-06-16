from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url: str = ''
    secret_key: str = ''
    algorithm: str = ''
    mail_username: str = ''
    mail_password: str = ''
    mail_from: str = ''
    mail_port: int = 465
    mail_server: str = ''
    redis_host: str = 'localhost'
    redis_port: int = 6379
    cloudinary_name: str = 'dnlxs1emv'
    cloudinary_api_key: str = '148257443743491'
    cloudinary_api_secret: str = 'zsNtk6Hflba7nHakEnZ6HocmEvk'

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()