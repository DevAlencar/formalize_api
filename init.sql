-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS formalize_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Grant privileges to the user
GRANT ALL PRIVILEGES ON formalize_db.* TO 'formalize_user'@'%';
FLUSH PRIVILEGES;
