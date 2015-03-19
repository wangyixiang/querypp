CREATE DATABASE ppbooks_db;
CREATE TABLE ppbooks (
    book_id serial PRIMARY KEY,
    book_name varchar NOT NULL,
    book_format varchar NOT NULL,
    book_raw_ed2k varchar NOT NULL,
    book_encoded_name varchar NOT NULL,
    is_valid boolean NOT NULL DEFAULT TRUE,
    is_downloadable boolean NOT NULL DEFAULT TRUE
);