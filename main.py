import japanize_kivy
from kivy.app import App
from kivy.uix.widget import Widget

class InputForm(Widget):
	pass

class Expense(Widget):
	pass

class MainApp(App):
	def build(self):
		return Expense()

if __name__ == "__main__":
	MainApp().run()