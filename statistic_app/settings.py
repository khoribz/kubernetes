from os import getenv

APP_HOST = getenv('APP_HOST', '0.0.0.0')
EXTERNAL_PORT = int(getenv('EXTERNAL_PORT', 80))
INTERNAL_PORT = int(getenv('INTERNAL_PORT', 4000))

POSTGRESQL_HOST = getenv('POSTGRESQL_HOST', 'postgres_container')
POSTGRESQL_PORT = int(getenv('POSTGRESQL_PORT', 5432))
POSTGRESQL_USER = getenv('POSTGRESQL_USER', 'postgres')
POSTGRESQL_PASSWORD = getenv('POSTGRESQL_PASSWORD', 'postgres')
POSTGRESQL_DATABASE = getenv('POSTGRESQL_DATABASE', 'statistics_app')

POSTGRES_STR_FOR_CONNECT = (
    f'postgresql+asyncpg://'
    f'{POSTGRESQL_USER}:'
    f'{POSTGRESQL_PASSWORD}@'
    f'{POSTGRESQL_HOST}:'
    f'{POSTGRESQL_PORT}/'
    f'{POSTGRESQL_DATABASE}'
)
