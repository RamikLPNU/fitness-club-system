from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+mysqlconnector://root:5885@localhost/fitness_club"
    # при потребі змініть


    class Config:
        env_file = ".env"


settings = Settings()