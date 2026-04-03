CREATE TABLE IF NOT EXISTS access_logs(
    id BIGSERIAL PRIMARY KEY,
    ip_address TEXT,
    event_time TEXT,
    method TEXT,
    endpoint TEXT,
    status_code INT,
    response_size INT
);