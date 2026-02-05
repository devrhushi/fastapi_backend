from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  #this is requred field not default value
  database_hostname: str
  database_port: str
  database_password: str
  database_name: str
  database_username: str
  secret_key: str 
  algorithm: str
  access_token_expire_minutes: str

  class Config:
    env_file = ".env" # tells pydantic to look for a .env file

settings = Settings()
