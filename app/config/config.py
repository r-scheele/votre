from pydantic import BaseSettings


class Settings(BaseSettings):
    # database configurations
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str

    # JWT
    secret_key: str
    algorithm: str
    access_token_expires_min: int

    class Config:
        env_file = ".env"
        orm_mode = True
