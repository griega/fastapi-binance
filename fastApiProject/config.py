from pydantic_settings import BaseSettings, SettingsConfigDict
import typing


class Settings(BaseSettings):

    def __getattr__(self, item):
        return self.__getattribute__(item)

    pg_host: str
    pg_user: str
    pg_password: str
    db_name: str
    pg_port: int
    convert_pairs_to_CG_syntax: typing.Dict[str, typing.Dict[str, str]]
    coin_pairs: typing.List[str]
    nats_subject: str
    nats_host: str
    nats_port: str
    redis_host: str
    redis_port: int
    wss_binance: str
    coingeko_url: str

    class Config:
        env_file = ".env"


settings = Settings()