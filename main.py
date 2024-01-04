import japanize_kivy
import sqlite3
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import ScreenManager, Screen

item_list = ["食費", "交通費", "書籍代", "娯楽費", "収入", "その他"]

class TotalForm(Screen):
	def get_total_from_database(self, start, end):
		if start == "":
			start = "1900-01-01"
		if end == "":
			end = "2100-01-01"
		print(start)
		print(end)
		sql = f"""
		SELECT acc_date,item_name,content,amount
		FROM acc_data as a,item as i
		WHERE a.item_code = i.item_code AND
		acc_date BETWEEN date('{start}') AND date('{end}')
		ORDER BY acc_date
		"""
		cursor = c.execute(sql)
		data = cursor.fetchall()
		sum = [0,0,0,0,0,0]
		for row in data:
			sum[item_list.index(row[1])] += int(row[3])
		self.ids.total_0.text = f"{item_list[0]}: ￥{sum[0]}"
		self.ids.total_1.text = f"{item_list[1]}: ￥{sum[1]}"
		self.ids.total_2.text = f"{item_list[2]}: ￥{sum[2]}"
		self.ids.total_3.text = f"{item_list[3]}: ￥{sum[3]}"
		self.ids.total_4.text = f"{item_list[4]}: ￥{sum[4]}"
		self.ids.total_5.text = f"{item_list[5]}: ￥{sum[5]}"
		

class DataTable(RecycleView):
	def get_data_from_database(self, start, end):
		self.data = []
		if start == "":
			start = "1900-01-01"
		if end == "":
			end = "2100-01-01"
		print(start)
		print(end)
		sql = f"""
		SELECT acc_date,item_name,content,amount
		FROM acc_data as a,item as i
		WHERE a.item_code = i.item_code AND
		acc_date BETWEEN date('{start}') AND date('{end}')
		ORDER BY acc_date
		"""
		cursor = c.execute(sql)
		data1 = cursor.fetchall()
		# テーブルヘッダーとデータを結合
		header = ['日付', '種別', '内訳', '金額']
		rows = [header] + list(data1)
		# データの表示
		for row in rows:
			for i in range(4):
				d = str(row[i])
				if i == 3 and d != "金額":
					d = f"￥{d}"
				self.data.append({'text': d})
		print(self.data)

class InputForm(Screen):
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
			VALUES(date('{date}'),{item_code},'{content}',{money})
			""")
			c.execute("COMMIT;")
			# 入力フォーム内のテキストを削除(重複登録防止)
			self.ids.input_date.text = ""
			self.ids.input_content.text = ""
			self.ids.input_money.text = ""
			print("1件登録しました")
		except:
			print("エラーにより登録できませんでした")

class OutputForm(Screen):
	pass



class MainApp(App):
	def build(self):
		self.dataTable_instance = DataTable()
		self.sm = ScreenManager()
		self.sm.add_widget(TotalForm(name='total'))
		self.sm.add_widget(InputForm(name='input'))
		self.sm.add_widget(OutputForm(name='output'))
		return self.sm
	


def create_database(c):
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
		c.execute("INSERT INTO item(item_name) VALUES('食費');")
		c.execute("INSERT INTO item(item_name) VALUES('交通費');")
		c.execute("INSERT INTO item(item_name) VALUES('書籍代');")
		c.execute("INSERT INTO item(item_name) VALUES('娯楽費');")
		c.execute("INSERT INTO item(item_name) VALUES('収入');")
		c.execute("INSERT INTO item(item_name) VALUES('その他');")
		c.execute("COMMIT;")
	except:
			pass


if __name__ == "__main__":
	# 空のデータベースを作成して接続する
	dbname = "database.db"
	c = sqlite3.connect(dbname)
	# 外部キー制約のオプションはデフォルトでは無効になっているため、これを有効にする
	c.execute("PRAGMA foreign_keys = 1")
	# データベース作成
	create_database(c)
	MainApp().run()