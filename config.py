from environs import Env


env = Env()
env.read_env()

DATABASE = {
    "host": env("DB_HOST"),
    "port": int(env("DB_PORT")),
    "user": env("DB_USER"),
    "password": env("DB_PASSWORD"),
    "database": env("DB_NAME"),
}

SERVER = {
    "host": env("HOST"),
    "port": env("PORT")
}