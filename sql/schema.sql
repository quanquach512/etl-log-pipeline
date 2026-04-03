CREATE TABLE IF NOT EXISTS access_logs(
    id BIGSERIAL PRIMARY KEY,
    ip_address TEXT NOT NULL,
    event_time TEXT NOT NULL,
    method TEXT NOT NULL,
    endpoint TEXT NOT NULL,
    status_code INT NOT NULL,
    response_size INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_access_log
    UNIQUE (ip_address, event_time, method, endpoint, status_code, response_size)
);

CREATE TABLE IF NOT EXISTS access_logs_staging(
ip_address TEXT,
    event_time TEXT,
    method TEXT,
    endpoint TEXT,
    status_code INT,
    response_size INT
);