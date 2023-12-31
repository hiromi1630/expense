import japanize_kivy
import sqlite3
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button

# 支出・収入種別のリスト
item_list = ["食費", "交通費", "書籍代", "娯楽費", "収入", "その他"]

class InputForm(Widget):
	# 家計簿登録処理
	def expense_register(self):
		# 日付を読み取る
		date = self.ids.input_date.text
		# 種別を読み取る
		item = self.ids.input_item_code.text
		item_code = item_list.index(item) + 1
		# 内訳を読み取る
		content = self.ids.input_content.text
		# 金額を読み取る
		money = self.ids.input_money.text
		try:
			c.execute(f"""
			INSERT INTO acc_data(acc_date, item_code, content, amount)
			VALUES('{date}',{item_code},'{content}',{money})
			""")
			c.execute("COMMIT;")
			# 入力フォーム内のテキストを削除(重複登録防止)
			self.ids.input_date.text = ""
			self.ids.input_content.text = ""
			self.ids.input_money.text = ""
			print("1件登録しました")
		except:
			print("エラーにより登録できませんでした")


class OutputForm(Widget):
	pass

class Expense(Widget):
	pass

class MainApp(App):
	def build(self):
		return Expense()

# データベース作成
def create_database():
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
			content TEXT NOT NULL,
			amount INTEGER NOT NULL,
			FOREIGN KEY(item_code) REFERENCES item(item_code)
		);
		"""
		# itemテーブルへリファレンスデータの登録
		c.execute(ddl)
		for i in item_list:
			c.execute(f"INSERT INTO item(item_name) VALUES('{i}');")
		c.execute("COMMIT;")
	except:
		pass


if __name__ == "__main__":
	create_database()
	MainApp().run()