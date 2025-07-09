CREATE USER calendar_admin WITH PASSWORD 'admin';
CREATE DATABASE calendar OWNER calendar_admin;
GRANT ALL PRIVILEGES ON DATABASE calendar TO calendar_admin;