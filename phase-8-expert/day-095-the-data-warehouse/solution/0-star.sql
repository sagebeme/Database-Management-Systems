-- A star schema beside the shop system:
--   dim_date:    date_key INT primary key (20260315 for 15 March 2026), day DATE, month INT, quarter INT, year INT,
--                weekday TEXT (Monday, Tuesday, ...), is_weekend BOOLEAN; all required.
--   dim_shop:    shop_key (identity, primary key), shop_id INT, name TEXT, county TEXT, valid_from DATE,
--                valid_to DATE (NULL while current), is_current BOOLEAN; all but valid_to required.
--   dim_product: product_key (identity, primary key), product_id INT, name TEXT, category TEXT; all required.
--   fact_sales:  date_key, shop_key and product_key (each required and referencing its dimension), qty INT and
--                revenue INT, both required.
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    day DATE NOT NULL,
    month INT NOT NULL,
    quarter INT NOT NULL,
    year INT NOT NULL,
    weekday TEXT NOT NULL,
    is_weekend BOOLEAN NOT NULL
);
CREATE TABLE dim_shop (
    shop_key INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    shop_id INT NOT NULL,
    name TEXT NOT NULL,
    county TEXT NOT NULL,
    valid_from DATE NOT NULL,
    valid_to DATE,
    is_current BOOLEAN NOT NULL
);
CREATE TABLE dim_product (
    product_key INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id INT NOT NULL,
    name TEXT NOT NULL,
    category TEXT NOT NULL
);
CREATE TABLE fact_sales (
    date_key INT NOT NULL REFERENCES dim_date (date_key),
    shop_key INT NOT NULL REFERENCES dim_shop (shop_key),
    product_key INT NOT NULL REFERENCES dim_product (product_key),
    qty INT NOT NULL,
    revenue INT NOT NULL
);
