CREATE KEYSPACE pageinfo WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };

USE pageinfo;

CREATE TABLE IF NOT EXISTS pages_by_domain (
    domain TEXT,
    page_id INT,
    title TEXT,
    created_at TIMESTAMP,
    PRIMARY KEY (domain, created_at)
) WITH CLUSTERING ORDER BY (created_at DESC);


CREATE TABLE IF NOT EXISTS pages_by_user (
    user_id INT,
    page_id INT,
    domain TEXT,
    title TEXT,
    created_at TIMESTAMP,
    PRIMARY KEY (user_id, created_at)
) WITH CLUSTERING ORDER BY (created_at DESC);

CREATE TABLE IF NOT EXISTS page_details (
    page_id INT PRIMARY KEY,
    domain TEXT,
    title TEXT,
    user_id INT,
    user_name TEXT,
    created_at TIMESTAMP,
    content_model TEXT,
    content_format TEXT,
    comment TEXT
);

CREATE TABLE IF NOT EXISTS user_activity (
    user_id INT,
    period_start TIMESTAMP,
    period_end TIMESTAMP,
    pages_count INT,
    PRIMARY KEY (user_id, period_start)
) WITH CLUSTERING ORDER BY (period_start DESC);
