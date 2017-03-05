from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ObjectProperty, NumericProperty, AliasProperty, StringProperty, ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.config import Config
from kivy.uix.listview import ListItemButton
from kivy.storage.jsonstore import JsonStore
from api import NotApi

api = NotApi()

store = JsonStore('data.json')


class LoginScreen(Screen):
	def giris(self):
		username = self.login.text
		password = self.password.text
		store.put('login', user=username, password=password)
		if api.checkuser(username, password):
			self.manager.get_screen('list').update()
			self.manager.transition = SlideTransition(direction="left")
			self.manager.current = 'list'


class NoteListScreen(Screen):
	new = False
	kulad = StringProperty()
	baslik = ListProperty()
	title = StringProperty()
	username = ''
	deneme = ''
	idnumber = ''
	title = ''
	info = ''
	def yeninot(self):
		self.new = True
		self.manager.get_screen('nots').clear()
		self.manager.transition = SlideTransition(direction="left")
		self.manager.current = 'nots'

	def cikis(self):
		self.manager.transition = SlideTransition(direction="right")
		self.manager.current = 'login'

	def notebutton(self, adapter):
		selection = adapter.selection[0].text
		idnumber = self.data[selection]
		data = api.notedetail(self.username, self.password, idnumber)
		(self.idnumber, self.title, self.info) = (data['id'], data['title'], data['info'])
		adapter.selection[0].deselect()
		adapter.selection = []
		self.manager.get_screen('nots').ids.note_title.text = self.title
		self.manager.get_screen('nots').ids.note_info.text = self.info
		self.manager.transition = SlideTransition(direction='left')
		self.manager.current = 'nots'

	def update(self):
		self.username = store.get('login')['user']
		self.password = store.get('login')['password']
		self.kulad = self.username
		self.data = api.notelist(self.username, self.password)
		self.baslik = list(self.data.keys())
		#self.id = list(self.data.values())
		self.ids['note_list_view'].adapter.bind(on_selection_change=self.notebutton)


class NoteScreen(Screen):
	def kaydet(self):
		if self.manager.get_screen('list').new:
			self.postnote()
			self.manager.get_screen('list').new = False
		else:
			self.editnote()
		self.manager.get_screen('list').update()	
		self.manager.transition = SlideTransition(direction="right")
		self.manager.current = 'list'

	def sil(self):
		if self.manager.get_screen('list').new == False:
			self.deletenote()
		self.manager.get_screen('list').new = False
		self.manager.get_screen('list').update()
		self.manager.transition = SlideTransition(direction="right")
		self.manager.current = 'list'

	def editnote(self):
		self.username = self.manager.get_screen('list').username
		self.password = self.manager.get_screen('list').password
		idnumber = self.manager.get_screen('list').idnumber
		title = self.ids.note_title.text
		info = self.ids.note_info.text
		api.putnote(self.username, self.password, idnumber, title, info)
	
	def deletenote(self):
		self.username = self.manager.get_screen('list').username
		self.password = self.manager.get_screen('list').password
		idnumber = self.manager.get_screen('list').idnumber
		api.deletenote(self.username, self.password, idnumber)

	def postnote(self):
		self.username = self.manager.get_screen('list').username
		self.password = self.manager.get_screen('list').password
		title = self.ids.note_title.text
		info = self.ids.note_info.text
		api.postnote(self.username, self.password, title, info)

	def clear(self):
		self.ids.note_title.text = ''
		self.ids.note_info.text = ''

class NoteButton(ListItemButton):
    index = NumericProperty(0)


class Manager(ScreenManager):
    login_screen = ObjectProperty(None)
    notelist_screen = ObjectProperty(None)
    note_screen = ObjectProperty(None)


class MyApp(App):
    title = 'CloudNote'


    def build(self):
        self.sm = Manager()
        return self.sm

if __name__ == '__main__':
    #Window.clearcolor = (1, 1, 1, 1)
    Window.size = (720,1280)
    MyApp().run()
