CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    category_id INTEGER,
    amount REAL,
    type TEXT CHECK(type IN ('income', 'expense')),
    FOREIGN KEY(category_id) REFERENCES categories(id)
);
