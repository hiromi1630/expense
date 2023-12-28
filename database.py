import sqlite3

# 空のデータベースを作成して接続する
dbname = "database.db"
c = sqlite3.connect(dbname)
# 外部キー制約のオプションはデフォルトでは無効になっているため、これを有効にする
c.execute("PRAGMA foreign_keys = 1")

# itemテーブルの定義
ddl = """
CREATE TABLE item
(
	item_code INTEGER PRIMARY KEY,
	item_name TEXT NOT NULL UNIQUE
);
"""
# SQLの発行
c.execute(ddl)

# acc_dataテーブルの定義
ddl = """
CREATE TABLE acc_data
( 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    acc_date DATE NOT NULL,
    item_code INTEGER NOT NULL,
    amount INTEGER,
    FOREIGN KEY(item_code) REFERENCES item(item_code)
);
"""
#SQLの発行
c.execute(ddl)
