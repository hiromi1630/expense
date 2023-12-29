import japanize_kivy
import sqlite3
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button

class InputForm(Widget):
	# 家計簿登録処理
	def expense_register(self):
		# 日付を読み取る
		date = self.ids.input_date.text
		# 内訳を読み取る
		item_code = self.ids.input_content.text
		# 金額を読み取る
		money = self.ids.input_money.text
		try:
			c.execute(f"""
			INSERT INTO acc_data(acc_date, item_code, amount)
			VALUES('{date}',{item_code},{money})
			""")
			c.execute("COMMIT;")
			self.ids.input_date.text = ""
			self.ids.input_content.text = ""
			self.ids.input_money.text = ""
			print("1件登録しました")
		except:
			print("エラーにより登録できませんでした")


class Expense(Widget):
	pass

class MainApp(App):
	def build(self):
		return Expense()

# 空のデータベースを作成して接続する
dbname = "database.db"
c = sqlite3.connect(dbname)
# 外部キー制約のオプションはデフォルトでは無効になっているため、これを有効にする
c.execute("PRAGMA foreign_keys = 1")

# 既にデータベースが存在する場合エラーになるので回避
try:    
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
    # itemテーブルへリファレンスデータの登録
    c.execute(ddl)
    c.execute("INSERT INTO item(item_name) VALUES('食費');")
    c.execute("INSERT INTO item(item_name) VALUES('交通費');")
    c.execute("INSERT INTO item(item_name) VALUES('書籍代');")
    c.execute("COMMIT;")
except:
    pass


if __name__ == "__main__":
	MainApp().run()