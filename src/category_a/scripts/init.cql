CREATE KEYSPACE wikistats WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };

USE wikistats;

CREATE TABLE hourly_stats (
    hour_start TIMESTAMP,
    hour_end TIMESTAMP,
    domain TEXT,
    page_count INT,
    PRIMARY KEY ((hour_start, domain))
);

CREATE TABLE bot_stats (
    time_start TIMESTAMP,
    time_end TIMESTAMP,
    domain TEXT,
    created_by_bots INT,
    PRIMARY KEY ((time_start, domain), created_by_bots)
);

CREATE TABLE user_stats (
    user_id TEXT,
    user_name TEXT,
    page_title TEXT,
    creation_time TIMESTAMP,
    PRIMARY KEY (user_id, creation_time)
);
