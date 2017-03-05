import requests
import json

class NotApi():
	def __init__(self):
		self.api_url = 'http://192.168.1.49:8000/api/'

	def checkuser(self, username, password):
		r = requests.get(self.api_url, auth=(username, password))
		if r.status_code == 200:
			#print(r.json())
			return True
		return False

	def notelist(self, username, password):
		r = requests.get(self.api_url, auth=(username, password))
		data = r.json()
		baslik = {}
		for i in data['results']:
			baslik[i['title']] = i['id']
		#print(list(baslik.keys()))
		return baslik

	def notedetail(self, username, password, idnumber):
		url = self.api_url + str(idnumber)
		r = requests.get(url, auth=(username, password))
		data = r.json()
		return data

	def putnote(self, username, password, idnumber, title, info):
		url = self.api_url + str(idnumber) + '/'
		r = requests.put(url, auth=(username, password), data={'title':title, 'info':info})
		print(r)
		if r.status_code == 200:
			return True
		return False

	def deletenote(self, username, password, idnumber):
		url = self.api_url +str(idnumber) + '/'
		r = requests.delete(url, auth=(username, password))
		if r.status_code == 200:
			return True
		return False

	def postnote(self, username, password, title, info):
		url = self.api_url
		r = requests.post(url, auth=(username, password), data={'title':title, 'info':info})
		if r.status_code == 200:
			return True
		return False

#api = NotApi()
#api.notelist('deneme', 'deneme')