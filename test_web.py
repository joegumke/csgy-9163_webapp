#from app.py import *
#from bs4 import BeautifulSoup
import requests, unittest

# UNITTEST all tests must start with test**
# LEVERAGE assert -> self.assertTrue()

# python3 test_web.py

WORDLIST = "wordlist.txt"
SITE = "http://localhost:5000/"

class TestWebFunctions(unittest.TestCase):

	def testRootPage(self):
		# This test validates that the Root Directory Page Response to a HTTP 200 Response Code
		loginPage = requests.get(SITE)
		assert(loginPage.status_code == 200)

	def test_validateLoginPage(self):
		# This test validates that the Login Page Response to a HTTP 200 Response Code
		loginPage = requests.get(SITE+"login")
		assert(loginPage.status_code == 200)

	def test_validateSpellCheckPage(self):
		# This test validates that the Spell Check Page Response to a HTTP 200 Response Code
		spellCheckPage = requests.get(SITE+"spell_check")
		assert(spellCheckPage.status_code == 200)

	def test_validateRegisterPage(self):
		# This test validates that the Register Page Response to a HTTP 200 Response Code
		registerPage = requests.get(SITE+"register")
		assert(registerPage.status_code == 200)


if __name__=='__main__':
	unittest.main()
	
