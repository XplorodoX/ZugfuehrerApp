CREATE TABLE delay
(
    date         DATE    NOT NULL,
    n            INTEGER NOT NULL,
    ar_time_diff VARCHAR,
    dp_time_diff VARCHAR,
    PRIMARY KEY (date, n)
);

CREATE TABLE delay_over_time
(
    n            INTEGER NOT NULL,
    c_date       DATE    NOT NULL,
    ar_time_diff VARCHAR,
    dp_time_diff VARCHAR,
    PRIMARY KEY (n, c_date)
);

CREATE TABLE avg_delay_at
(
    n            INTEGER NOT NULL,
    ar_time_diff VARCHAR,
    dp_time_diff VARCHAR,
    PRIMARY KEY (n)
);