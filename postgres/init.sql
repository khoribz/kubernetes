SELECT 'CREATE DATABASE statistics_app'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'statistics_app');

GRANT ALL PRIVILEGES ON DATABASE statistics_app TO postgres;