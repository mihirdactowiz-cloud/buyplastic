import mysql.connector
import json

def connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="actowiz",
        database="buyplastic"
    )
    return conn, conn.cursor()


# PRODUCT URL TABLE
def create_product_urls_table():
    conn, cur = connection()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS product_urls(
        id INT AUTO_INCREMENT PRIMARY KEY,
        product_url TEXT,
        status VARCHAR(50) DEFAULT 'pending'
    )
    """)
    conn.commit()
    cur.close()
    conn.close()


def insert_product_url(product_url):
    conn, cur = connection()
    query = """
    INSERT INTO product_urls(
        product_url,
        status
    )
    VALUES(%s,%s)
    """
    cur.execute(query, (product_url, "pending"))
    conn.commit()
    cur.close()
    conn.close()


def get_pending_urls():
    conn, cur = connection()
    cur.execute("""
    SELECT product_url
    FROM product_urls
    WHERE status='pending'
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [i[0] for i in rows]


def update_status(product_url, status):
    conn, cur = connection()
    query = """
    UPDATE product_urls
    SET status=%s
    WHERE product_url=%s
    """
    cur.execute(query, (status, product_url))
    conn.commit()
    cur.close()
    conn.close()


# PRODUCTS TABLE
def create_products_table():
    conn, cur = connection()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS products(
        id INT AUTO_INCREMENT PRIMARY KEY,
        product_name TEXT,
        product_url TEXT,
        product_entity_id BIGINT,
        variant_entity_id BIGINT,
        sku VARCHAR(255),
        price FLOAT,
        stock BOOLEAN,
        variant_json JSON
    )
    """)
    conn.commit()
    cur.close()
    conn.close()

def insert_product(data):
    conn, cur = connection()
    query = """
    INSERT INTO products(
        product_name,
        product_url,
        product_entity_id,
        variant_entity_id,
        sku,
        price,
        stock,
        variant_json
    )
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        data["product_name"],
        data["product_url"],
        data["product_entity_id"],
        data["variant_entity_id"],
        data["sku"],
        data["price"],
        data["stock"],
        json.dumps(data["variants"])
    )
    cur.execute(query, values)
    conn.commit()
    cur.close()
    conn.close()