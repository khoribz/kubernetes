import os

APP_HOST = os.getenv('APP_HOST', 'app')
APP_PORT = os.getenv('APP_PORT', '80')
GET_STATISTICS_DELAY = 5  # sec
STATISTICS_FILE_NAME = 'statistics.json'
