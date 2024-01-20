def create_tables(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        order_date DATE NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
    """)


def add_product(cursor, name, category, price):
    params = (name, category, price)
    cursor.execute("""
    INSERT INTO products (name, category, price) VALUES
    (?, ?, ?)
    """, params)
    return cursor.lastrowid


def add_customer(cursor, first_name, last_name, email):
    params = (first_name, last_name, email)
    cursor.execute("""
    INSERT INTO customers (first_name, last_name, email) VALUES
    (?, ?, ?)
    """, params)
    return cursor.lastrowid


def place_an_order(cursor, customer_id, product_id, quantity, date):
    params = (customer_id, product_id, quantity, date)
    cursor.execute("""
    INSERT INTO orders (customer_id, product_id, quantity, order_date) VALUES
    (?, ?, ?, ?)
    """, params)
    return cursor.lastrowid


def get_sum_of_orders(cursor):
    results = cursor.execute("""
    SELECT SUM(orders.quantity * products.price)
    FROM orders
    INNER JOIN products ON products.product_id = orders.product_id
    """).fetchone()[0]

    return results


def get_order_number_by_client(cursor):
    results = cursor.execute("""
    SELECT
      customers.first_name,
      customers.last_name,
      SUM(orders.quantity)
    FROM customers
    INNER JOIN orders ON orders.customer_id = customers.customer_id
    GROUP BY customers.customer_id
    """).fetchall()
    
    return results


def get_average_order(cursor):
    results = cursor.execute("""
    SELECT AVG(orders.quantity * products.price)
    FROM orders
    INNER JOIN products ON products.product_id = orders.product_id
    """).fetchone()
    
    return results[0]


def get_most_popular_category(cursor):
    results = cursor.execute("""
    SELECT products.category
    FROM products
    INNER JOIN orders ON orders.product_id = products.product_id
    GROUP BY products.category
    ORDER BY COUNT(orders.product_id) DESC
    LIMIT 1
    """).fetchone()
    
    return results[0]


def get_number_of_products_in_category(cursor):
    results = cursor.execute("""
    SELECT category, COUNT(category)
    FROM products
    GROUP BY category
    """).fetchall()
    
    return results

def make_technology_more_expensive(cursor):
    cursor.execute("""
    UPDATE products
    SET price = price * 1.1
    WHERE category = "Technology"
    """)